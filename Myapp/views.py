from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User, auth

from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth import authenticate
from .forms import RegForm, conForm, QForm
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,SetPasswordForm
# Create your views here.
from .models import Blog,Comment,Contact,Question,Answer,Like, BlogView,Category,Tag, Profile, LikeContent, Report, Notification
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import RawQuerySet 
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import RegForm, UpdateProfileForm, ReportForm
from django.http import HttpResponse
from formtools.wizard.views import SessionWizardView
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import update_session_auth_hash
import os
from django_htmx.http import HttpResponseClientRedirect
from render_block import render_block_to_string
from django.core.mail import send_mail, BadHeaderError
from verify_email.email_handler import send_verification_email


# Create your views here.

class ProfileView(SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'profilePic/'))
    form_list = [RegForm,UpdateProfileForm]
    template_name = 'registration.html'
    # Do something with the cleaned_data, then redirect
    # to a "success" page.
    def done(self, form_list,**kwargs):
        
        user_form = form_list[0]
        username = user_form.cleaned_data.get('username')
        
        print(username)
        if form_list:
            user_form.save()
            userr = User.objects.get(username__icontains=username)
            profile = form_list[1].save(commit=False)
            inactive_user = send_verification_email(self.request, user_form)
        
            profile.username =  userr
            profile.save()
        

            messages.info(self.request, " please check your email to verify your account")
            return redirect('login')
        
        else:
            print("something is wrong ")
            
        return redirect('index')

def about(request):
    users = User.objects.all()
    unumb = users.count
    answer = Answer.objects.all()
    anumb = answer.count
    blog = Blog.objects.all()
    bnumb = blog.count
    question =  Question.objects.all()
    qnumb = question.count
    return render(request, 'about-us.html',{'unumb':unumb,'anumb':anumb,'bnumb':bnumb,'qnumb':qnumb})

def register(request):
 
    if request.user.is_authenticated:
        return redirect('index')
     
    if request.method == 'POST':
        form = RegForm(request.POST)
 
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request=request,username = username,password = password)
            auth.login(request, user)
            return redirect('index')
         
        else:
            return render(request,'registration.html',{'form':form})
     
    else:
        form = RegForm()
        return render(request,'registration.html',{'form':form})


def login(request):

    if request.user.is_authenticated:
        return redirect('index')
     
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
 
        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.error(request,'user not authorized')
            return redirect('login')
     
    else:
        form = AuthenticationForm()
        return render(request, 'signin.html', {'form':form})


def logout(request):
    auth.logout(request)
    return redirect('login')

def index(request):
    
    
    notify = Notification.objects.filter(username=request.user.username,isread="Unread")
    blog = Blog.objects.all()
    
    return render(request, 'index.html', {'blog': blog,'notify':notify})

def blogs(request):
    notify = Notification.objects.filter(username=request.user.username,isread="Unread")
    blog = Blog.objects.all()
    blogi = Blog.objects.all().order_by('id')[:3]
    search  = request.GET.get('search')
    if search:
        blog =  Blog.objects.filter(title__icontains = search)
    
    category = Category.objects.annotate(blog_count=Count('blog'))
    tag = Tag.objects.all()
    # django = Blog.object.filter(category_id =)
    page = request.GET.get('page', 1)

    paginator = Paginator(blog, 3)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
   
    
    return render(request, 'blog.html', {'blogdetails': blogi,
        'cat':category,'tag':tag, 'page_obj':page_obj,'notify':notify})


def answer(request):
    notify = Notification.objects.filter(username=request.user.username,isread="Unread")
    blog = Question.objects.all()
    tag = Tag.objects.all()
    
    search  = request.GET.get('search')
    if search:
        blog =  Question.objects.filter(title__icontains = search)
    
    category = Category.objects.annotate(blog_count=Count('blog'))
    # django = Blog.object.filter(category_id =)
    page = request.GET.get('page', 1)

    paginator = Paginator(blog, 4)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    
    return render(request, 'answer.html', {'blogdetails': blog,'page_obj':page_obj,'cat':category,
    'tag':tag,'notify':notify
    })

def blog(request, slug):
    # try:
        
        if request.user.is_active and request.user.is_authenticated:
            notify = Notification.objects.filter(username=request.user.username,isread="Unread")
            category = Category.objects.annotate(blog_count=Count('blog'))
            tag = Tag.objects.all()
            blogdetails = Blog.objects.all().order_by('id')[:3]
            blog = Blog.objects.get(slug=slug)
            usar = User.objects.get(username__icontains = "Admin")
            if usar:
                profile = usar
            else:
                profile = Profile.objects.get(username=blog.username)
            like = LikeContent.objects.filter(blog=blog, username=request.user)
            clike = LikeContent.objects.filter(blog=blog).count()
            views = BlogView.objects.filter(blog=blog).count()
            blog.views += 1
            blog.save()
            user = User.objects.get(id=blog.username_id)
            comm = Comment.objects.filter(blog_id=blog)
            number = comm.count()
            com = Comment()
            username = request.POST.get('user')
            post = request.POST.get('blog')
            comment = request.POST.get('comment')
        # if username :
        #     messages.error(request,'you are not authorized')
        #     return redirect('register')
        # else:
        

            if request.method == 'POST':
                com.username_id = username
                com.blog_id = post
                com.comment = comment
                com.save()
                return HttpResponseRedirect(reverse("blog",args={blog.slug}))
        
            return render(request, 'blogdetails.html', {'blog': blog,'user':user,'number':number,'comm':comm,
            'views':views,'blogdetails':blogdetails, 'cat':category,
            'profile':profile,'like':like,'clike':clike,'tag':tag,
            'notify':notify
            })
        else:
            messages.error(request, 'you are not logged in')
            return render(request, 'blogdetails.html')

    # except:
    #     messages.error(request,'you are not authorized to comment, register to do so')
    #     return redirect('register')

def view(request, slug):
    blog = Question.objects.get(slug=slug)
    if request.user.is_active and request.user.is_authenticated:
        blogdetails = Blog.objects.all().order_by('id')[:3]
        notify = Notification.objects.filter(username=request.user.username,isread="Unread")
        category = Category.objects.annotate(blog_count=Count('blog'))
        tag = Tag.objects.all()
        
        profile = Profile.objects.get(username=blog.username)
        user = User.objects.get(id=blog.username_id)
        very = Answer.objects.select_related('question__username').filter(question=blog, username_id=request.user.id)
        comm = Answer.objects.filter(question_id=blog).order_by('id')
    
        answerr =  Like.objects.filter(answer__question=blog).filter( username=request.user)
        
        
        answer = Like.objects.raw('SELECT id, answer_id FROM Myapp_like WHERE username_id ='+ str(request.user.id))
       
            
        comma = Answer.objects.all()
        number = comm.count()
        
        com = Answer()
        
        ans = request.POST.get('ans')
        print("this is answer id ",ans)
        username = request.POST.get('user')
        post = request.POST.get('blog')
        
        comment = request.POST.get('comment')

    # else:
    
        if request.method == 'POST':
            com.username_id = username
            if com.username_id == user:
                messages.error(request, 'you cannot reply your own question')
                return HttpResponseRedirect(reverse("view",args={blog.slug}))
            else:
            

                Notification.objects.create(
                            username = blog.username,
                            user = request.user.username,
                            topic = "answer your question",
                            notify = "/view/",
                            ids = blog.slug


                    )
                com.question_id = post
                com.comment = comment
                print(com.comment)
                com.save()
                return HttpResponseRedirect(reverse("view",args={blog.slug}))
        # for i in Answer.objects.raw('SELECT id, question_id FROM Myapp_answer WHERE username_id = ' + str(request.user.id)):
        #     print(i.username.username,"make sense")
        #     print(i.id)
        # try:
        #     c = Like.objects.filter(answer_id=i.id, username_id = request.user.id)
        #     for b in c:
        #         print('na b',b)
        # except ObjectDoesNotExist:
        #         c = None
        
        return render(request, 'questiondetails.html', {'blog': blog,'user':user,'number':number,'comm':comm,
            'com':com,'answer':answer,'user_liked': answerr,'tag':tag,'notify':notify,'profile':profile,'very':very,
            'cat':category,'blogdetails':blogdetails,
                                        
    
        }
        )
    else:
        messages.error(request,'log in to see question and answers provided')
        return render(request, 'questiondetails.html', {'blog': blog})
    #     
    # except:
    #     messages.error(request,'you are not authorized to answer, register to do so')

        # return redirect('register')

# def like(request, slug):

#     blog = Question.objects.get(slug=slug)
#     post = get_object_or_404(Answer, id=request.POST.get('blogger'))
#     liker = Like()
#     print("this is post", post)
#     ha = request.POST.get('blogger')
#     # post = Answer.objects.get(id=ha)
#     print('this is post id,',post.id)
#     username = request.user
#     current_like = post.likes
#     if liker.username_id==username:
#         messages.error(request, ' you cannot like you own comment')
#         return HttpResponseRedirect(reverse("view",args={blog.slug}))
#     liked = Like.objects.filter(username=username,answer=post).exists()
#     if not liked:
#         Like.objects.create(username=username,answer=post)
#         messages.info(request,"you don add a like")
#         current_like = current_like + 1

#     else:
#         Like.objects.filter(username=username,answer=post).delete()
#         current_like = current_like - 1
#         messages.info(request,"you don comot a like")
#     post.likes = current_like
#     post.save()

#     return HttpResponseRedirect(reverse("view",args={blog.slug}))
#     # return render(request, 'view.html',{'liked':liked})
#     HttpResponseRedirect(request.path)




# def like(request, slug):
#     blog = Question.objects.get(slug=slug)
#     post = get_object_or_404(Answer, id=request.POST.get('blogger'))
#     username = request.user
#     current_like = post.likes
#     liked = Like.objects.filter(username=username, answer=post).exists()
#     if not liked:
#         Like.objects.create(username=username, answer=post)
#         action = 'like'
#         messages.info(request,"you don add a like")
#         current_like = current_like + 1
#     else:
#         Like.objects.filter(username=username, answer=post).delete()
#         action = 'unlike'
#         current_like = current_like - 1
#         messages.info(request,"you don comot a like")
#     post.likes = current_like
#     # post.save()
#     return redirect(request.META.get('HTTP_REFERER'))

# def like(request, slug):
#     if request.user.is_active and request.user.is_authenticated:
        
#             blog = Question.objects.get(slug=slug)
#             post = get_object_or_404(Answer, id=request.POST.get('blogger'))
#             user = request.user

#             current_like = post.likes
#             if post.liker.filter(answer=post).exists():
#                 print(user, "for many to manjy ")
#                 messages.info(request,"you don comot a like")
#                 post.liker.remove(user)
#                 liked = False
#                 # return HttpResponseRedirect(reverse("view",args={blog.slug}))
#             else:
#                 post.liker.add(user)

#                 liked = True
#                 # return HttpResponseRedirect(reverse("view",args={blog.slug}))
#             # try:
#             #     like = Like.objects.get(answer=post, username=user)
#             #     current_like = current_like - 1
#             #     messages.info(request,"you don comot a like")
#             #     like.delete()
#             # except Like.DoesNotExist:
#             #     Like.objects.create(answer=post, username=user)
#             #     current_like = current_like + 1
            
#             return HttpResponseRedirect(reverse("view",args={blog.slug}))
#     else:
#         messages.error(request, 'you are not logged in')
#         return HttpResponseRedirect(reverse("view",args={blog.slug}))
        
def like(request, slug):
    if request.user.is_active and request.user.is_authenticated:
        blog = Question.objects.get(slug=slug)
        if request.method == "GET":
            answer_id = request.GET.get('blogger')
            ids = request.GET.get('blogo')
            usa = request.GET.get('usa')
            title = request.GET.get('title')
            user = request.user
            answer = get_object_or_404(Answer, id=answer_id)
            print(answer.username)
            print(request.user.username)
            if request.user.id == answer.username_id:
                messages.error(request, 'you are cannot upvote your answer')
                # return redirect(request.META.get('HTTP_REFERER'))
                return HttpResponseRedirect(reverse("view",args={blog.slug}))
            else:
        
                if user in answer.liker.all():

                    Notification.objects.filter(user=request.user.username, notify=title).delete()
                    
                    answer.liker.remove(user)
                    # liked = False
                else:
                
                
                    Notification.objects.create(
                                    username = answer.username,
                                    user = request.user.username,
                                        topic = "upvote your answer",
                                        notify = '/view/',
                                        ids = ids


                                )
                    answer.liker.add(user)
                        
                        # liked = True

                context = {
                    'likes_count': answer.liker.count(),
                    # 'liked': liked,
                }
                # return JsonResponse(context)
                # return redirect(request.META.get('HTTP_REFERER'))
                return HttpResponseRedirect(reverse("view",args={blog.slug}))
    else:
        messages.error(request, "you aint logged in ")
        return redirect('login')



def like_content(request, slug):
    if request.user.is_active and request.user.is_authenticated:
        blog = get_object_or_404(Blog, slug=slug)
        c= Notification.objects.filter(username=request.user, user=request.user)
        if c.exists():
            print("nothing ")
        else:
            Notification.objects.create(
                            username = blog.username,
                            user = request.user.username,
                                topic = "like your content",
                                notify = "/blog/",
                                ids = blog.slug


                        )
        LikeContent.objects.create(username=request.user, blog=blog)
        return HttpResponseClientRedirect(reverse("blog",args={blog.slug}))
    
    else:
        return render(request,template_name="error.html")

def unlike_content(request, slug):
    if request.user.is_active and request.user.is_authenticated:
        blog = get_object_or_404(Blog, slug=slug)
        Notification.objects.filter(user=request.user.username, ids=blog.slug).delete()
        LikeContent.objects.filter(username=request.user, blog=blog).delete()
        return HttpResponseClientRedirect(reverse("blog",args={blog.slug}))
    else:
        return render(request,template_name="error.html")




def profile(request, username):
    if request.user.is_superuser:
        messages.error(request, 'you are not authorized, log in as user not admin')
        return redirect('login')
    elif request.user.is_authenticated and request.user.is_active and not request.user.is_superuser:
        notify = Notification.objects.filter(username=request.user.username,isread="Unread")
        userr = get_object_or_404(User, username=username)
        profiler = Profile.objects.get(username=userr)
        print(userr.username)
        question = Question.objects.filter(username_id=userr.id)
        qnumb = question.count()
        answer = Answer.objects.filter(username=userr)
        answerr = answer.count()
        blog = Blog.objects.filter(username=userr)
        bnumb = blog.count()
        if request.method == "POST":
            form = UpdateProfileForm(request.POST, request.FILES, instance=userr.profile)
           
    #       {{content|safe }}
            if form.is_valid():
                
                
                messages.success(request, 'Profile successfully Created')
                form.save()
                return HttpResponseRedirect(reverse("profile",args={userr.username}))
            
            else:
                messages.error(request, 'you can only create profile once but you can edit multiple times')
                return HttpResponseRedirect(reverse("profile",args={userr.username}))
        else:
            form = UpdateProfileForm(instance=userr.profile, )

        return render(request,"profile.html",
                    {'question':question,'answer':answerr,
                    'blog':blog,'qnumb':qnumb,'bnumb':bnumb,
                    'ans':answer,'form':form,'userr':userr,
                    'profile':profiler,'notify':notify
                    }
                    )
    
    else:
        messages.error(request, 'you are not authorized')
        return redirect('login')

def updateprofile(request, username):
    user = User.objects.get(username=username)
    if request.method == 'POST':
        # user_form = RegForm(request.POST, instance=user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=user.profile)

        if  profile_form.is_valid():
            # user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            # return HttpResponseRedirect(reverse("updateprofile", args={'user'}))
            return HttpResponse(
               f"{user} updated. reload profile to see changes"
                    
            )
    else:
        # user_form = RegForm(instance=user)
        profile_form = UpdateProfileForm(instance=user.profile, )

    return render(request, 'updateprofile.html', {
        # 'user_form': user_form,
          'profile_form': profile_form,'user':user})


# def update(request, slug):
#     product = get_object_or_404(Question, slug=slug)
#     if request.method == "POST":
#         form = QForm(request.POST,request.FILES, instance=product)
#         if form.is_valid():
#             # status = form.cleaned_data['status']
#             # username = form.cleaned_data['username']
#             messages.success(request, 'updated successfully')
#             form.save()
#             return redirect('profile')
#     else:
#         form = QForm(instance=product)
#     return render(request, 'uploaded.html', {
#         'form': form,
#         'product': product,
#     })


def contact(request):
    contact = Contact()
    if request.method =="POST":
        name = request.POST.get('name')
        print("na name be this ", name)
        email = request.POST.get('email')
        comment = request.POST.get('message')
        if name == request.user.is_superuser:
            print("yesss oo na admin")
        if name !=request.user.username:
            print("oooooleeee")
            return redirect('contact')
        elif email != request.user.email:
            print("oooooleeee twoo")
            return redirect('contact')
        elif name == request.user.is_superuser:
            print("oooooleeee three")
            return redirect('contact')
        else:
             
            
            contact.name = name
            contact.email = email
            contact.message = comment
            # contact.save()
            return redirect('contact')
    return render(request,'contact.html')
        
def create(request):
    if request.user.is_active and request.user.is_authenticated:
        notify = Notification.objects.filter(username=request.user.username,isread="Unread")
        if request.method == "POST":
            
            form = conForm(request.POST, request.FILES)
    #       {{content|safe }}
            if form.is_valid():
                title = request.POST.get('title')
                body = request.POST.get('body')
                print(title)
                if Blog.objects.filter(title=title):
                    messages.error(request, 'Blog already exist')
                    return redirect('create')
                elif len(body)  < 255:
                    messages.error(request, 'your content is too small ')
                    return redirect('create')
                else:
                    messages.success(request, 'content created successfully')
                    form.save()
                    return redirect('create')
            
            else:
                print('some thing is wromh')
                return redirect('create')
        
        
        else:
            form = conForm(initial = {'username':request.user.id,'title':request.user.username})
            return render(request,'create.html',{'form':form,'notify':notify})
    else:
        messages.error(request, 'log in to create content')
        return redirect('login')
    
def question(request):
    if request.user.is_active and request.user.is_authenticated:
        notify = Notification.objects.filter(username=request.user.username,isread="Unread")
        if request.method == "POST":
            
            form = QForm(request.POST, request.FILES)
    #       {{content|safe }}
            if form.is_valid():
                title = request.POST.get('title')
                body = request.POST.get('body')
                if Blog.objects.filter(title=title):
                    messages.error(request, 'Question has been asked')
                    messages.error(request, 'check question and answer page')
                    return redirect('answer')
                
                else:
                    messages.success(request, 'Question successfully inquired')
                    form.save()
                    return redirect('question')
            
            else:
                print('some thing is wromh')
                return redirect('question')
        
        
        else:
            form = QForm(initial = {'username':request.user.id,})
            return render(request,'question.html',{'form':form,'notify':notify})
    else:
        messages.error(request, 'login to ask a question')
        # form = QForm(initial = {'username':request.user.id})
        return redirect('login')
    

def update(request, slug):
    product = get_object_or_404(Question, slug=slug)
    if request.method == "POST":
        form = QForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            # status = form.cleaned_data['status']
            # username = form.cleaned_data['username']
            messages.success(request, 'updated successfully')
            form.save()
            return redirect('profile')
        else:
            messages.error(request, 'your update wasnt successfuly ')
            return HttpResponseRedirect(reverse("update", args={'product.slug'}))
    else:
        form = QForm(instance=product)
    return render(request, 'update.html', {
        'form': form,
        'product': product,
    })

def tag(request, slug):
    search = request.GET.get('search')
    tag = Tag.objects.get(slug=slug)
    if search:
        question = Question.objects.filter(tag=tag,title__icontains = search)
    else:

        question = Question.objects.filter(tag=tag)
    return render(request, 'tag.html', {'tag':tag,'question':question})

def category(request, slug):
  
    search = request.GET.get('search')
    cat = Category.objects.get(slug=slug)
    if search:
        blog = Blog.objects.filter(category=cat,title__icontains = search)
    else:

        blog = Blog.objects.filter(category=cat)
    return render(request, 'cat.html', {'cat':cat,'blog':blog})


# @login_required



def report(request):
    if request.user.is_active and request.user.is_authenticated:
        notify = Notification.objects.filter(username=request.user.username,isread="Unread")
        if request.method == "POST":
            form = ReportForm(request.POST, request.FILES)
    #       {{content|safe }}
            if form.is_valid():
                culprit = request.POST.get('culprit')
                type = request.POST.get('type')
            
                if Report.objects.filter(username=request.user, culprit=culprit):
                    messages.error(request, f'{culprit} already reported')
                    return redirect('report')
                elif User.username!=culprit:
                    messages.error(request, f'{culprit} doesnt not exists')
                    return redirect('report')
            
                else:
                    
                    messages.success(request, 'report created successfully')
                    form.save()
                    return redirect('report')
            
            else:
                print('some thing is wromh')
                return redirect('report')
        
        
        else:
            form = ReportForm(initial = {'username':request.user.id})
            return render(request,'report.html',{'form':form,'notify':notify})
    else:
        return render(request, 'error.html')
        
def read(request):
    like = request.POST.get('like')
    print("this is like ",like)
    notify = get_object_or_404(Notification, id=like,username=request.user.username)
    notify.isread = "Read"
    notify.save()
    return redirect(request.META.get('HTTP_REFERER'))
    # next_url = request.GET.get('next', '/')

    # Redirect the user to the 'next' page
    # return redirect(next_url)


def changepassword(request):
    if request.method == 'POST':
        
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SetPasswordForm(request.user)
    return render(request, 'changepassword.html', {
        'form': form
    })





def like_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    user = request.user
    liked = False
    if blog.likes.filter(id=user.id).exists():
        blog.likes.remove(user)
    else:
        blog.likes.add(user)
        liked = True
    context = {'liked': liked}
    return JsonResponse(context)