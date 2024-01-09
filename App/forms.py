from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profiles
from django import forms
# from django import request
from django.db.models import fields
from django.utils.text import slugify
from django_countries.widgets import CountrySelectWidget
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
from django import forms
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import Accordion, AccordionGroup
from django_select2.forms import Select2MultipleWidget
from phonenumber_field.formfields import PhoneNumberField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column,Field, Button
from django_countries.fields import CountryField
# from django_countries.fields import CountryField
from django import forms
from .models import Picture
from django.contrib.auth.models import User, auth
from django.contrib.auth import login,authenticate
from django_select2 import forms as s2forms

class RegForm(UserCreationForm):

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter valid Email'}))
    email = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter valid Email'}))
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
            if email and User.objects.filter(email=email).exists():
                self.add_error('email', 'This email address is already in use.')
        except ValidationError:
            raise forms.ValidationError('Enter a valid email address(e.g. Example@hello.com')
        return email
    # def clean(self):
    #     cleaned_data = super().clean()
    #     email = cleaned_data.get('email')

    #     if email and User.objects.filter(email=email).exists():
    #         self.add_error('email', 'This email address is already in use.')

    #     return cleaned_data

    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1' ,'password2' )



class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    cover = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    about = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    phone = PhoneNumberField(
        widget=PhoneNumberInternationalFallbackWidget(attrs={
            'placeholder': 'Enter valid Phone number',
            'class': 'form-control'
        }),
        
    )
    country = CountryField(blank_label='Select country').formfield(widget=CountrySelectWidget(attrs={'class': 'form-control'}))
    # country = CountryField(blank_label="(Select country)")
    class Meta:
        model = Profiles
        fields = fields = {'avatar','about','country','cover','phone'}
        # widget = {"country": CountrySelectWidget()}
    def __init__(self, *args, **kwargs):
        super(UpdateProfileForm, self).__init__(*args, **kwargs)
        # self.fields['country'].empty_label = "select country"
        # self.fields['username'].widget = forms.HiddenInput()




class PictureUpdate(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    cover = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    about = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    
  
    class Meta:
        model = Profiles
        fields = fields = {'avatar','about','cover'}
        # widget = {"country": CountrySelectWidget()}



class TwoEdit(forms.ModelForm):
    phone = PhoneNumberField(
        widget=PhoneNumberInternationalFallbackWidget()
        
    )
    country = CountryField(blank_label='Select country').formfield(widget=CountrySelectWidget(attrs={'class': 'form-control'}))

    class Meta:
        model = Profiles
        fields = fields = {'country','phone'}
    





# class PictureForm(forms.ModelForm):
    # tagged_friends = s2forms.ModelSelect2MultipleWidget(queryset=Profiles.objects.all())
    
class PictureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(PictureForm, self).__init__(*args, **kwargs)
        profile = Profiles.objects.get(username=self.request.user)
        friends = profile.friends.all()
        self.fields['tagged_users'].queryset = friends

    tagged_users = forms.ModelMultipleChoiceField(
        queryset=Profiles.objects.none(),
        widget=Select2MultipleWidget,
        required=False
    )

    class Meta:
        model = Picture
        fields = ['title', 'description', 'image', 'tagged_users']




class EditForm(forms.ModelForm):
    username =forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    email =forms.EmailField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    first_name=forms.CharField( max_length=30, required=True)
    last_name=forms.CharField( max_length=30, required=True)

    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
    
    def clean_email(self):
            # Get the email
        username = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.exclude(pk=self.instance.pk).get(username=username)
            
            
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return username

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')



 
# class conForm(forms.ModelForm):
#     class Meta:
#         model= Blog
#         fields = '__all__'
    
#     def __init__(self, *args, **kwargs):
#         super(conForm, self).__init__(*args, **kwargs)
        
#         self.fields['username'].widget = forms.HiddenInput()
#         # self.slug = slugify(self.fields)
#         self.fields['views'].widget = forms.HiddenInput()
#         self.fields['likes'].widget = forms.HiddenInput()
#         self.fields['category'].empty_label = "select category"
        
# class QForm(forms.ModelForm):
#     class Meta:
#         model= Question
#         widgets = {
#           'body': forms.Textarea(attrs={'rows':4, 'cols':15}),
#         }
#         fields = '__all__'
    
#     def __init__(self, *args, **kwargs):
#         super(QForm, self).__init__(*args, **kwargs)
#         self.fields['username'].widget = forms.HiddenInput()
#         self.fields['tag'].empty_label = "select tag"
        
        

# class ReportForm(forms.ModelForm):
#     culprit = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Enter the person's name"}))
#     class Meta:
#         model = Report
#         fields ="__all__"

#     def __init__(self, *args, **kwargs):
#         super(ReportForm, self).__init__(*args, **kwargs)
#         self.fields['username'].widget = forms.HiddenInput()
#         self.fields['status'].widget = forms.HiddenInput()






# class FollowerForm(forms.ModelForm):
 
#     class Meta:
#         model = Follower
#         fields = "__all__"
#         # widget = {"country": CountrySelectWidget()}
#     # def __init__(self, *args, **kwargs):
#     #     super(UpdateProfileForm, self).__init__(*args, **kwargs)
#     #     # self.fields['country'].empty_label = "select country"
#     #     self.fields['username'].widget = forms.HiddenInput()