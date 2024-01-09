from django.contrib.auth import authenticate
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,SetPasswordForm
# Create your views here.
# from .models import Blog,Comment,Contact,Question,Answer,Like, BlogView,Category,Tag, Profile, LikeContent, Report, Notification
from Myapp.models import Profile
from .models import Picture, Tags, Profiles, FriendRequest, Chatt
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import RawQuerySet 
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from App.forms import RegForm, UpdateProfileForm, PictureForm, EditForm, TwoEdit, PictureUpdate
from django.http import HttpResponse
from formtools.wizard.views import SessionWizardView
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import update_session_auth_hash
import os
from django_htmx.http import HttpResponseClientRedirect
from django.views.decorators.cache import cache_control
from django.core.mail import send_mail, BadHeaderError
from verify_email.email_handler import send_verification_email
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import PictureForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.urls import reverse
from online_users.models import OnlineUserActivity
from datetime import datetime, timedelta
from django.contrib.auth.forms import PasswordChangeForm
# import datetime
from django.utils import timezone
# Create your views here.

def get_online_users():
    # Get session keys of active sessions
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())

    # Get user IDs from active sessions
    user_ids = [session.get_decoded().get('_auth_user_id') for session in active_sessions]

    # Retrieve User objects for online users
    User = get_user_model()
    online_users = User.objects.filter(id__in=user_ids)

    return online_users

@login_required(login_url='/App/login/')
def post(request):
    if request.user:
        if Profile.objects.filter(username = request.user):
            messages.error(request, "user not authorized")
            return redirect('/Myapp/login/')
        
    return render(request, 'App/post.html')
    # return HttpResponse('<div> i am post {{request.user.username}} </div>')


class ProfileView(SessionWizardView):
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'social/profilePic/'))
    # form_list = [RegForm,PictureUpdate,UpdateProfileForm] for as many as possible steps 
    form_list = [RegForm,UpdateProfileForm]
    template_name = 'App/registration.html'
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
            # inactive_user = send_verification_email(self.request, user_form)
        
            profile.username =  userr
            profile.save()
        

            messages.info(self.request, " account created successfully ")
            return redirect('login')
        
        else:
            print("something is wrong ")
            
        return redirect('post')
    


# def login(request):

#     if request.user.is_authenticated:
#         return redirect('post')
     
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username =username, password = password)
#         profile = Profile.objects.get(username=user)
#         if profile:
#             messages.info(request, f'{user.username} you registered as a developer not a socialist')
#             return redirect('/MyApp/login/')
#         if user is not None:
#             auth.login(request,user)
#             return redirect('post')
#         else:
#             messages.error(request,'user not authorized')
#             return redirect('login')
     
#     else:
#         form = AuthenticationForm()
#         return render(request, 'App/login.html', {'form':form})


def login(request):

    if request.user.is_authenticated:
        return redirect('App:post')
     
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
        profile = Profile.objects.filter(username=user)
        if profile:
            messages.info(request, f'{user.username} you registered as a developer not a socialist')
            return redirect('/Myapp/login/')
 
        elif user is not None:
            auth.login(request,user)
            return redirect('App:post')
        else:
            messages.error(request, 'invalid login details')
            form = AuthenticationForm()
            return render(request,'App/login.html',{'form':form})
     
    else:
        form = AuthenticationForm()
        return render(request, 'App/login.html', {'form':form})


@login_required(login_url='/App/login/')
def picture(request):
    if Profile.objects.filter(username = request.user):
        messages.error(request, "you are not authorized")
        return redirect("/Myapp/login")
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            picture = form.save(commit=False)
            picture.user = request.user
            # picture.save()

            # Save many-to-many relationships with user IDs
            tagged_users = form.cleaned_data['tagged_users']
            for user in tagged_users:
                print("Username:", user.username)
                print("User ID:", Profiles.objects.get(username_id=user.id))
                tags = Profiles.objects.get(username_id=user.id)
                picture.save()
                picture.tagged_users.add(tags)


          
            return redirect('/App/post')
        else:
            print("something went wrong")
    else:
        form = PictureForm(request=request)
    return render(request, 'App/picupload.html', {'form': form})

@login_required(login_url='/App/login/')
def all(request):
    if Profile.objects.filter(username = request.user):
        messages.error(request, "you are not authorized")
        return redirect("/Myapp/login")
    
    users = Profiles.objects.all()
    

    return render(request, 'App/all.html',{'users':users})

@login_required(login_url='/App/login/')
def add(request):
    if Profile.objects.filter(username = request.user):
        messages.error(request, "you are not authorized")
        return redirect("/Myapp/login")
    
    if request.user.is_active and request.user.is_authenticated:
    
        friend = FriendRequest()
        if request.method == "POST":
            sender = request.POST.get('sender')
            
            recipient = request.POST.get('recipient')
            profiles = get_object_or_404(Profiles, username_id=recipient)
            print(" this is sender ", sender)
            if FriendRequest.objects.filter(sender=sender, recipient=recipient).exists():
                messages.info(request, "you already sent a request")
                return redirect('/App/all/')
            elif sender == request.user.id:
                messages.error(request, 'you cannot add yourself ')
                return redirect('/App/all/')
            
            elif FriendRequest.objects.filter(sender=recipient, recipient=sender).exists():
                messages.info(request, f" {profiles.username} already sent you a request")
                return redirect('/App/all/')
            else:
                friend.sender = request.user
                friend.recipient = profiles.username
                messages.info(request, "request successfully sent ")
                friend.save()

    
                return redirect('/App/all/')
    else:
        return redirect('/App/login/')        

@login_required(login_url='/App/login/')
def accept(request,username):
    if Profile.objects.filter(username = request.user):
        messages.error(request, "you are not authorized")
        return redirect("/Myapp/login")
    
    if request.user.is_active and request.user.is_authenticated:
    
        use = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profiles, username=use)
        geting =  Profiles.objects.filter(username=use)
        profiles = FriendRequest.objects.filter(recipient=request.user.id)
        if request.user == profile.username:
            if request.method == "POST":
                sender =  request.POST.get('sender')
            
                adder = get_object_or_404(Profiles, username=sender)
                if sender in profile.friends.all():
                    messages.error(request, 'you have accepted request')
                else:
                    messages.success(request, 'friend request accepted ')
                    
                    profile.friends.add(sender)
                    adder.friends.add(profile.username)
                    adder.save()
                    profile.save()
                    return redirect("App:accept", username=profile.username)
                    # return HttpResponseRedirect(reverse("App:accept", args=(profile.username)))

            else:
                print("something sup ")
        
            
            return render(request, 'App/accept.html', {'profiles':profiles, 'profile':profile, 'geting':geting})
        else:
            return redirect('/App/login/')
    else:
        return redirect('/App/login/')

@login_required(login_url='/App/login/')
def chats(request):
    if Profile.objects.filter(username = request.user):
        messages.error(request, "you are not authorized")
        return redirect("/Myapp/login")
    
    
    users = Profiles.objects.get(username = request.user)
    last_message = Chatt.objects.filter(
        Q(sender=request.user, receiver=users.username) |
        Q(sender=users.username, receiver=request.user)
    ).last()
    return render(request, 'App/chats.html', {'users':users,'last':last_message  })

@login_required(login_url='/App/login/')
def conversation(request, username):
    if Profile.objects.filter(username = request.user):
        messages.error(request, "you are not authorized")
        return redirect("/Myapp/login")
    
    users = Profiles.objects.get(username = request.user)
    current = get_object_or_404(User, username=username)
    profile = Profiles.objects.get(username=current)  
    online_users = OnlineUserActivity.get_user_activities(timedelta(minutes=5))
    current_online = (user for user in online_users)
    chatts = Chatt()
    
    history = Chatt.objects.filter(title__icontains=request.user.username,sender=request.user,receiver=profile.username).order_by('timer') | Chatt.objects.filter(title__icontains=profile.username.username, sender=profile.username,receiver=request.user).order_by('timer')
    phistory = Chatt.objects.filter(
        Q(sender=profile.username) & Q(receiver=request.user)

    ).order_by('timer')
    last_message = Chatt.objects.filter(
        Q(sender=request.user, receiver=profile.username) |
        Q(sender=profile.username, receiver=request.user)
    ).last()
    # is_friend = users.friends.filter(username=profile.username).exists()
    # print("this is the current user ",is_friend.username)

    pform=EditForm(instance=request.user)
    eform = TwoEdit(instance=users)
    picform = PictureUpdate(request.POST, request.FILES, instance=users)
    form = PasswordChangeForm(request.user)
    if request.method == "POST":
        pform=EditForm(request.POST,instance=request.user)
        eform = TwoEdit(request.POST,instance=users)
        picform = PictureUpdate(request.POST,instance=users)

        
        if pform.is_valid() and eform.is_valid():
            pform.save()
            eform.save()
            messages.add_message(request,messages.SUCCESS, f'Updated Successfully')
            
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            pform=EditForm(instance=request.user)
            eform = TwoEdit(instance=users)
            picform = PictureUpdate(instance=users)
            print("something is wrong")
            # return redirect(request.META.get('HTTP_REFERER'))
            

        text = request.POST.get("text")
        chatts.title = request.user.username + profile.username.username
        
        chatts.sender = request.user
        chatts.receiver = profile.username
        chatts.conversation = text
        if chatts.conversation == "" or chatts.conversation ==  " ":
            print("not possible")
            return redirect("App:conversation", username=profile.username)
        else:
        
            chatts.save()
            Profiles.objects.filter(username = request.user).update(last_activity=timezone.now())  # Update the last_activity for the logged-in user's friend
            Profiles.objects.filter(username=current).update(last_activity=timezone.now())  # Update the last_activity for the friend's profile
            
       
            return redirect("App:conversation", username=profile.username)
        
        

        


    return render(request, 'App/chat-1.html', {'profile': profile, 'history': history, 'phistory': phistory, 'users':users,
            'last':last_message,'online_users': online_users,
            'online':current_online,'pform':pform,'eform':eform,'picform':picform,'form':form
            
                                        })

@login_required(login_url='/App/login/')
def chatting(request, username):
    if Profile.objects.filter(username = request.user):
        messages.error(request, "you are not authorized")
        return redirect("/Myapp/login")
    
    current = get_object_or_404(User, username=username)
    profile = Profiles.objects.get(username=current)
    chatts = Chatt()

    if request.method == "POST":
        text =  request.POST.get("text")
        chatts.sender = request.user
        chatts.receiver = profile.username
        chatts.conversation = text
        chatts.save()
        return redirect("App:Chattting", username=profile.username)
    return render(request, 'App/sender.html', {'profile':profile})




@login_required(login_url='/App/login/')
def dashboard(request):
    if Profile.objects.filter(username = request.user):
        messages.error(request, "you are not authorized")
        return redirect("/Myapp/login")
    
    userr = User.objects.get(username = request.user)
    
    users = Profiles.objects.get(username = request.user)
    
        
    pform=EditForm(instance=request.user)
    eform = TwoEdit(instance=users)

    if request.method == "POST":
        pform=EditForm(request.POST,instance=request.user)
        eform = TwoEdit(request.POST,instance=users)

        
        if pform.is_valid() and eform.is_valid():
            pform.save()
            eform.save()
            messages.add_message(request,messages.SUCCESS, f'Updated Successfully')
            
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            pform=EditForm(instance=request.user)
            eform = TwoEdit(instance=users)
            print("something is wrong")
       
            context={
            'pform':pform,
        
            }
        return redirect(request.META.get('HTTP_REFERER'))
    
        
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/App/login/')
def PictureUpdate(request):
    if Profile.objects.filter(username = request.user):
        messages.error(request, "you are not authorized")
        return redirect("/Myapp/login")
    
    userr = User.objects.get(username = request.user)
    
    users = Profiles.objects.get(username = request.user)
    
      
    picform = PictureUpdate(instance=users)

    if request.method == "POST":
     
        picform = PictureUpdate(request.POST,instance=users)
        if picform.is_valid():
            picform.save()
            
            messages.add_message(request,messages.SUCCESS, f'Updated Successfully')
            
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            pform=EditForm(instance=request.user)
            eform = TwoEdit(instance=users)
            print("something is wrong")
        
            context={
            'picform':picform,
        
            }
        return redirect(request.META.get('HTTP_REFERER'))
    
        
    return redirect(request.META.get('HTTP_REFERER'))



def change_password(request):
    if Profile.objects.filter(username = request.user):
        messages.error(request, "you are not authorized")
        return redirect("/Myapp/login")
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    
        
    return redirect(request.META.get('HTTP_REFERER'))




def logout(request):
    auth.logout(request)
    messages.info(request, 'Come back soon')
    return redirect('/App/login/')





