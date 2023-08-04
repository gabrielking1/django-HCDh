from django.contrib import admin
from App.models import Profiles, Picture, Chatt
# Register your models here.

@admin.register(Profiles)
class ProfilesAdmin(admin.ModelAdmin):
    list_display = ( 'username',)

@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ( 'user',)

@admin.register(Chatt)
class ChattAdmin(admin.ModelAdmin):
    list_display = ( 'sender','receiver')