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
    public = forms.BooleanField(initial=True, required=True)
    # start_time = forms.DateTimeField()
    # end_time = forms.DateTimeField()
    # created_at = forms.DateTimeField(auto_now_add=True)
    # updated_at = forms.DateTimeField(auto_now=True)
