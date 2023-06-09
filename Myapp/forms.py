from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Blog,Question, Profile, Report
from django import forms
# from django import request
from django.db.models import fields
from django.utils.text import slugify
from django_countries.widgets import CountrySelectWidget
# from django_countries.fields import CountryField


class RegForm(UserCreationForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1' ,'password2' )
	# def save(self, commit=True):
	# 	user = super(RegForm, self).save(commit=False)
	# 	user.email = self.cleaned_data['email']
	# 	if commit:
	# 		user.save()
	# 	return user
 
class conForm(forms.ModelForm):
    class Meta:
        model= Blog
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(conForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget = forms.HiddenInput()
        # self.slug = slugify(self.fields)
        self.fields['views'].widget = forms.HiddenInput()
        self.fields['likes'].widget = forms.HiddenInput()
        self.fields['category'].empty_label = "select category"
        
class QForm(forms.ModelForm):
    class Meta:
        model= Question
        widgets = {
          'body': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(QForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.HiddenInput()
        self.fields['tag'].empty_label = "select tag"
        
        

class ReportForm(forms.ModelForm):
    culprit = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Enter the person's name"}))
    class Meta:
        model = Report
        fields ="__all__"

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.HiddenInput()
        self.fields['status'].widget = forms.HiddenInput()



class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    # country = CountryField(blank_label="(Select country)")
    class Meta:
        model = Profile
        fields = fields = {'avatar','bio','state','phone'}
        # widget = {"country": CountrySelectWidget()}
    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        # self.fields['country'].empty_label = "select country"
        # self.fields['username'].widget = forms.HiddenInput()