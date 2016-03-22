from django.shortcuts import render
from django.db import transaction
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from plaza.forms import *


# Create your views here.

############################################## Functionality #############################################

####### Login/register #######

@transaction.atomic
def register(request):
	# Use django form to register user, validate emails
	# We could use exactly what we did for registration in homework
	# Following is just a copy from my homework
	# TODO: Have some default profile picture for new users if they do not upload
	#       Option to register as staff (for staff, might need code) or student

    context = {}
    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'register.html', context)

    
    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email'])
    
    # Mark the user as inactive to prevent login before email confirmation.
    new_user.is_active = False
    new_user.save()

    new_user_profile, created = UserProfile.objects.get_or_create(user=new_user)
    new_user_profile.save()

    # # Email validation
    # token = default_token_generator.make_token(new_user)
    # email_body = """
    # Welcome to the Social Network.  Please click the link below to
    # verify your email address and complete the registration of your account:

    #   http://%s%s
    # """ % (request.get_host(), reverse('confirm', args=(new_user.username, token)))

    # send_mail(subject="Verify your email address",
    #           message= email_body,
    #           from_email="jiachens@andrew.cmu.edu",
    #           recipient_list=[new_user.email])
    # context['email'] = form.cleaned_data['email']
    # return render(request,'needs-confirmation.html',context)

    # Logs in the new user and redirects to the home page
    new_user= authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])
    login(request, new_user)
    return redirect(reverse('home'))



@transaction.atomic
def confirm_registration(request, username, token):
	# confirm registration 
	# TODO: have a better confirmation page than hw6 
    return

def login(request):
	# Not sure if this is needed. For previous homework, we can redirect to "auth_views.login" in url
	# If we want perform some pre-check of login credential or add some verification, we might nedd this function.
	# Also, we could let users to login using their SNS account (fb, twitter etc.)
    return

####### For course_create_page #######

# @login_required
# @transaction.atomic
# def create_course(request):
# 	# Creation of a new course

####### For team_create_page #######

# @login_required
# @transaction.atomic
def create_team(request):
 	# Creation of a new team 
 	# Email notification to targer students
 	# Two different ways of team formation
    return


####### For administration_page #######

@login_required
@transaction.atomic
def create_tags(request):
	# Create a tag for students to follow
    return

@login_required
@transaction.atomic
def delete_tags(request, id):
	# Delete a tag
    return

@login_required
@transaction.atomic
def delete_post(request):
	# Delete a post, only for staff 
    return

@login_required
@transaction.atomic
def delete_comment(request):
	# Delete a post, only for staff 
    return

####### For home_page #######

@login_required
@transaction.atomic
def make_post(request):
	# Publish a new post
    return

@login_required
@transaction.atomic
def make_comment(request):
	# Publish a new comment
    return

@login_required
@transaction.atomic
def upvote(request):
	# Upvote a post
    return

@login_required
@transaction.atomic
def downvote(request):
	# Downvote a post
    return

@login_required
@transaction.atomic
def follow_tag(request):
	# Follow a specific tag
    return

@login_required
@transaction.atomic
def unfollow_tag(request):
	# unfollow a specific tag
    return

####### For ajax  #######
def get_post(request):
	# With specification of what posts to get (all or just those have specific tags) and how the post is going to 
	# be sorted (by number of upvotes or date or length)
    return


def get_notication(request):
	# Get new notification in all pages (notifications is in homepage, but for other pages, just do it 
	# as a dropdown from nav bar. Another good way is to use push notification library such as Parse
    return

####### For resource page #######

@login_required
@transaction.atomic
def upload_resource(request):
	#  Staff only
    return


####### Other functionalities #######
@login_required
def get_notification(request, id):
	# Edit content
	# Change visibility
	# Assign to students
    return



@login_required
@transaction.atomic
def edit_post(request, id):
	# Edit content
	# Change visibility
	# Assign to students
    return

@login_required
@transaction.atomic
def edit_course(request, id):
	# Edit general settings
    return

@login_required
def search(request):
	# Search for keywords, time, tags
	# Popup (modal in bootstrap) previous posts before someone wants to ask questions contains some similar content
	return

# More to be added 

############################################## Display pages #############################################


@login_required
def home_page(request):
    # With different users, display either home/staff home page
    return render(request, "home.html",{})


# @login_required
def staffhome_page(request, id):
    # With different users, display either home/staff home page
    return render(request, "staff_home.html",{})

# @login_required
def profile_page(request, id):
	# Show profile page of "id"
	return render(request, "profile.html", {})

@login_required
def edit_profile_page(request, id):
	# Show the page of editing self profile
	return

@login_required
def administration_page(request, id):
	# Show the page of administration (link to course_creation)
	# This is only accessible by staffs (from staff_home_page)
	return


@login_required
@transaction.atomic
def course_creation_page(request):
	# Show the page to create courses
	# This is only accessible by staffs (actuallt it could be integrated into administration page as a dropdown panel)
	return

# @login_required
@transaction.atomic
def team_creation_page(request):
	# Show the page to create teams
	return render(request, "team_creation.html", {})

def resource_page(request):
	# Show the page of resources (notes, videos)
	# For staff, there's an optiona for uploading new resources
	return render(request, "resources.html", {})

@login_required
def resource_slide_page(request):
	# Show the page a slide (could be a pdf slide, or just streaming the video)
	# Students could post comments to each slide / video
	return

