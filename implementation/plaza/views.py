import json

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from plaza.forms import *
from django.contrib.auth import login, authenticate, update_session_auth_hash
from plaza.models import *
from django.core import serializers

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
    new_user.save()
    new_person, created = Person.objects.get_or_create(user=new_user)
    new_person.save()

    # # Email validation
    # token = default_token_generator.make_token(new_user)
    # email_body =
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

def clogin(request):
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
def submit_team(request):
    if not request.is_ajax():
        if request.method != 'POST':
            # respond with error
            return HttpResponse("Request is not valid", status=404)

    # TODO: fix error messages
    team_name = request.POST.get("team_name", "")
    team_members = json.loads(request.POST.get("team_members",""))
    assignment_number = request.POST.get("assignment_number", "")
    course_number = request.POST.get("course_number", "")

    if (team_name == "" or team_members == "" or
        course_number == "" or assignment_number == ""):
        return HttpResponse("No team name provided", status=400)

    # TODO: race condition in this case
    for member in team_members:
        person = Person.objects.get(user__username=member);
        if person == None:
            return HttpResponse("Team member does not exist", status=400)
        teams = person.teams
        if teams != None:
            if teams.filter(assignment__number=assignment_number).count() != 0:
                return HttpResponse("Person is already in a team", status=400)

    course = get_object_or_404(Course,id=course_number)
    course_assignments = course.assignments
    assignment = course_assignments.get(number=assignment_number)

    if assignment == None:
        return HttpResponse("Assignment does not exist", status=400)

    team = Team(team_name=team_name, assignment=assignment, members=team_members)
    team.save()


    # TODO: send notifications
    send_notifications(message, '/myteam/'+course_number+'/'+assignment_number+'/', team_members)

    json_obj = {
            "message":"Team "+team_name+" created!"
            }

    return HttpResponse(json.dumps(json_obj), content_type='application/json')

####### For administration_page #######

# Mrigesh's part starts here

@login_required
def forum(request, id):
    # View all posts (unfiltered)
    # id refers to the course ID
    return


@login_required
@transaction.atomic
def post(request):
    # Create new post


@login_required
@transaction.atomic
def delete_post(request, id):
    # Delete a post
    return

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

# Mrigesh's part ends here

# used in dynamic teammate searching/adding
def search_student(request):
    if not request.is_ajax():
        if request.method != 'POST':
            # respond with error
            return HttpResponse("Request is not valid", status=404)


    username = request.POST.get("username","")

    if username == "":
        return HttpResponse("Username not provided", status=404)

    user_acc = get_object_or_404(User, username__exact=username)

    json_obj = {
            "username": username,
            "userid": user_acc.id
        }

    return HttpResponse(json.dumps(json_obj), content_type='application/json')


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

# Used to send notifications to a list of people
@login_required
def send_notifications(message, redirect_url, receivers):
    # TODO: implement soon
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


# @login_required
# @transaction.atomic
def course_creation_page(request):
	# Show the page to create courses
	# This is only accessible by staffs (actuallt it could be integrated into administration page as a dropdown panel)
    context = {}
    if request.method == 'GET':
        return render(request, "course_creation.html", {})
    form = CourseForm(request.POST)
    # if form.is_valid():
    number = request.POST["number"]
    name = request.POST["name"]
    semester = request.POST["semester"]
    description = request.POST["description"]
    maxenroll = request.POST["maxenroll"]
    print number,name,semester,description,maxenroll
    # public = request.POST["public"]
    course = Course(number=number, name=name, semester=semester,description=description,max_enroll=maxenroll)
    course.save()
    print "Course created"
    return redirect(reverse('home'))

# @login_required
@transaction.atomic
def staff_team_page(request, id):
	# Show the page to create teams
	return render(request, "staff_team_view.html", {})

# @login_required
@transaction.atomic
def team_creation_page(request, course_number, assignment_number):
    context = {"course_number": course_number, "assignment_number":assignment_number}
    return render(request, "team_creation.html", context)

def resource_page(request):
	# Show the page of resources (notes, videos)
	# For staff, there's an optiona for uploading new resources
	return render(request, "resources.html", {})

@login_required
def resource_slide_page(request):
	# Show the page a slide (could be a pdf slide, or just streaming the video)
	# Students could post comments to each slide / video
	return

