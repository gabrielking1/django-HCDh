from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
app_name = 'App'
urlpatterns = [
    path('post/', views.post, name='post'),
    path('register/', views.ProfileView.as_view(), name="register"),
    path('login/',views.login, name='login'),
    path('picture/', views.picture, name='picture'),
    path("select2/", include("django_select2.urls")),
    path('all/', views.all, name="all"),
    path('chats/', views.chats, name="chats"),
    path('add/', views.add, name="add"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.logout, name='logout'),
    path('accept/<str:username>', views.accept, name = 'accept'),
    path('chatting/<str:username>', views.chatting, name = 'chatting'),
    path('conversation/<str:username>', views.conversation, name = 'conversation'),
    path('change_password', views.change_password, name='change_password'),

    
]

# urlpatterns = urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# urlpatterns = urlpatterns+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) 