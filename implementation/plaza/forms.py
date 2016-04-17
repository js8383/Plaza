from django import forms

from django.contrib.auth.models import User
from django.core.validators import validate_email
from models import *

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

class CourseForm(forms.Form):
    number = forms.CharField(max_length=10, required=True)
    name = forms.CharField(max_length=128, required=True)
    semester = forms.CharField(max_length=3, required=True) # Create choices
    description = forms.CharField(max_length=160, required=True)
    maxenroll = forms.IntegerField(required=False)
    public = forms.BooleanField(initial=True, required=False)

    def clean(self):
        cleaned_data = super(CourseForm, self).clean()
        course_num = cleaned_data['number']
        if Course.objects.filter(number=course_num).count() != 0:
            raise forms.ValidationError("Course already exists")

class PersonForm(forms.Form):
    first_name = forms.CharField(max_length=20, label='First Name', required=True)
    last_name = forms.CharField(max_length=20, label='Last Name', required=True)
    nickname = forms.CharField(max_length=32, label='Nick Name', required=True)
    date_of_birth = forms.DateField(label="Date of Birth", required=False)
    gender = forms.CharField(max_length=6, label='Gender', required=False)
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

        person.first_name = self.cleaned_data.get('first_name')
        person.last_name = self.cleaned_data.get('last_name')
        person.nickname = self.cleaned_data.get('nickname')
        person.short_bio = self.cleaned_data.get('short_bio')
        person.date_of_birth = self.cleaned_data.get('date_of_birth')
        person.profile_image = self.cleaned_data.get('profile_image')
        
        user.save()
        person.save()
        return user