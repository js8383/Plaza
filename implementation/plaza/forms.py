from django import forms

from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.forms import ModelForm
from models import *
from datetime import datetime
from tinymce.widgets import TinyMCE

MAX_UPLOAD_SIZE = 2500000

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name  = forms.CharField(max_length=20)
    username   = forms.CharField(max_length = 20)
    email      = forms.CharField(max_length = 40,
                                 validators = [validate_email])
    password1  = forms.CharField(max_length = 200,
                                 label='Password',
                                 widget = forms.PasswordInput())
    password2  = forms.CharField(max_length = 200,
                                 label='Confirm password',
                                 widget = forms.PasswordInput())


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username

class CourseSignupForm(forms.Form):
    access_code = forms.IntegerField()

class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields=['number', 'name', 'semester', 'description',
                'max_enroll', 'access_code', 'public']

# TODO: add more validation
class PersonForm(forms.Form):
    first_name = forms.CharField(max_length=20, label='First Name', required=True)
    last_name = forms.CharField(max_length=20, label='Last Name', required=True)
    nickname = forms.CharField(max_length=32, label='Nick Name', required=False)
    email = forms.CharField(max_length = 40, validators = [validate_email])
    date_of_birth = forms.DateField(label="Date of Birth", required=False)
    gender = forms.CharField(max_length=6, label='Gender', required=False)
    field = forms.CharField(max_length=32, label='Field', required=False)
    institution = forms.CharField(max_length=32, label='Institution',required=False)
    short_bio = forms.CharField(max_length=1024, label="Short Bio", required=False)
    profile_image = forms.ImageField(label='Profile Image', required=False)

    def clean_profile_image(self):
        image = self.cleaned_data['profile_image']
        if not image:
            print "Not a image"
            return None
        if not image.content_type or not image.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if image.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return image

    def save(self, user, person):
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')

        person.nickname = self.cleaned_data.get('nickname')
        person.date_of_birth = self.cleaned_data.get('date_of_birth')
        person.gender = self.cleaned_data.get('gender')
        person.field = self.cleaned_data.get('field')
        person.institution = self.cleaned_data.get('institution')
        person.short_bio = self.cleaned_data.get('short_bio')
        if not self.cleaned_data.get('profile_image') == None:
            person.profile_image = self.cleaned_data.get('profile_image')
        user.save()
        person.save()
        return user

class PostForm(forms.Form):
    title       = forms.CharField(max_length=128)
    text        = forms.CharField(widget=TinyMCE(attrs={'cols': 85, 'rows': 10,'class':'form-control'}))
    post_type   = forms.MultipleChoiceField(choices=Post.POST_CHOICES)

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        return

class ResourceFileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ResourceFileForm, self).__init__(*args, **kwargs)
        self.fields['notes'].required = False
        # self.fields['file'].required = False
        self.fields['tags'].required = False
        self.fields['due'].required = False

    class Meta:
        model = Resource
        fields = ('title','notes', 'file', 'tags', 'due',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "",'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'placeholder': "", 'style': 'resize:none;', 'rows':'4', 'class': 'form-control'}),
            'file': forms.FileInput(attrs={'placeholder': "",'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'due': forms.DateInput(attrs={'placeholder': "", 'id':'dpicker', 'class': 'form-control'}),
        }
        labels = {
            'title': 'Title',
            'notes': 'Notes',
            'file': 'Attach File',
            'tags':'Tags',
            'due': 'Due'
        }

    def clean(self):
        cleaned_data = super(ResourceFileForm, self).clean()
        return cleaned_data


class ResourceFolderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(ResourceFolderForm, self).__init__(*args, **kwargs)
        self.fields['notes'].required = False

    class Meta:
        model = Resource
        fields = ('title','notes',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "",'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'placeholder': "", 'style': 'resize:none;', 'rows':'4', 'class': 'form-control'}),

        }
        labels = {
            'title': 'Title',
            'notes': 'Notes',
        }

    def clean(self):
        cleaned_data = super(ResourceFolderForm, self).clean()
        return cleaned_data

class ChangePasswordForm(forms.Form):
    opassword  = forms.CharField(max_length = 200,
                                 label='Old Password',
                                 widget = forms.PasswordInput())
    npassword1  = forms.CharField(max_length = 200,
                                 label='New Password',
                                 widget = forms.PasswordInput())
    npassword2  = forms.CharField(max_length = 200,
                                 label='Confirm New Password',
                                 widget = forms.PasswordInput())
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(ChangePasswordForm, self).clean()

        # Confirms that the two password fields match
        opassword = cleaned_data.get('opassword')
        npassword1 = cleaned_data.get('npassword1')
        npassword2 = cleaned_data.get('npassword2')
        if npassword1 and npassword1 and npassword1 != npassword2:
            raise forms.ValidationError("New passwords did not match.")
        if opassword and opassword == npassword1:
            raise forms.ValidationError("Your new passwords should be different from the old one.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data
    
