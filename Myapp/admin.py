from django.contrib import admin
from .models import Blog,Category,Question,Tag,Answer,Like,Profile, Type, Report,Notification
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'slug')
    prepopulated_fields = {'slug': ('category',)}

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('username', 'title',)
    readonly_fields = (
        'username','title','body'
    )
    # prepopulated_fields = {'slug': ('title',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'slug')
    # prepopulated_fields = {'slug': ('tag',)}

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('username', 'title',)
    readonly_fields = (
        'username','title','body','tag',
    )
    # prepopulated_fields = {'slug': ('title',)}
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('username', 'question','likes')
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'state','bio')
# admin.site.register(Answer)
admin.site.register(Like)

class TypeAdmin(admin.ModelAdmin):
    list_display = ('username',)
# admin.site.register(Answer)
admin.site.register(Type)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('username', 'type','status')
# admin.site.register(Answer)
admin.site.register(Report)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ( 'username',)