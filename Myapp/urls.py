from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.index, name='index'),
    path('about/', views.about, name='about'),
    path('blog/<slug:slug>', views.blog, name = 'blog'),
    path('view/<slug:slug>', views.view, name = 'view'),
    path('tag/<slug:slug>', views.tag, name = 'tag'),
    path('category/<slug:slug>', views.category, name = 'category'),
    # path('like/<slug:slug>', views.like, name = 'like'),
    path('like/', views.like, name = 'like'),
    path('profile/<str:username>', views.profile, name = 'profile'),
    path('login/',views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # path('register/', views.register, name="register"),
    path('register/', views.ProfileView.as_view(), name="register"),
    path('contact/', views.contact, name = 'contact'),
    path('create/', views.create, name = 'create'),
    path('report/', views.report, name = 'report'),
    path('blogs/', views.blogs, name = 'blogs'),
    path('question/', views.question, name = 'question'),
    path('answer/', views.answer, name = 'answer'),
    path('update/<slug:slug>', views.update, name='update'),
    path('like_content/<slug:slug>', views.like_content, name='like_content'),
    path('unlike_content/<slug:slug>', views.unlike_content, name='unlike_content'),
    path('updateprofile/<str:username>', views.updateprofile,name='updateprofile'),
    path('read/', views.read, name = 'read'),
    path('changepassword/',views.changepassword, name='chnagepassword')
    
]

urlpatterns = urlpatterns+static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)