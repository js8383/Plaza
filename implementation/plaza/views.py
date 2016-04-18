import json

from django.core.exceptions import ObjectDoesNotExist
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

###### For course_edit page #######

@login_required
@transaction.atomic
def remove_person_from_course(request):
    if not request.is_ajax():
        if request.method != 'POST':
            # respond with error
            return HttpResponse("Request is not valid",
                                content_type="application/json",
                                status=404)

    course_number = request.POST.get("course_number", "")
    course_semester = request.POST.get("course_semester", "")
    username = request.POST.get("username", "")
    role = request.POST.get("role", "")

    if (course_number == "" or course_semester == "" or
        username == "" or role == ""):
        return HttpResponse("Invalid parameters", content_type="application/json", status=400)

    course = get_object_or_404(Course, number=course_number, semester=course_semester)

    if role == 'instructor':
        group = course.instructors
    elif role == 'staff':
        group = course.staff
    elif role == 'student':
        group = course.students
    else:
        return HttpResponse("Invalid parameters", content_type="application/json", status=400)

    # if we are removing an instructor, we need to check
    # that there are more in the course
    if role == 'instructor':
        if course.instructors.count() == 1:
            return HttpResponse("Can't remove last instructor",
                    content_type="applicaiton/json",
                    status=400)

    user = get_object_or_404(User, username__exact=username)

    # remove the person from the group if they exist

    if group.filter(username__exact=username).count() != 0:
        group.remove(user)
    else:
        return HttpResponse("Not a member", content_type="application/json", status=400)

    message = ("You have been removed from " + course_number + " " + course_semester +
               " as a " + role + ".")

    # TODO: send notifications to user

    json_obj = {
            "first_name":user.first_name,
            "last_name":user.last_name
            }

    return HttpResponse(json.dumps(json_obj), content_type='application/json')

@login_required
@transaction.atomic
def save_course_pref(request, course_number, course_semester):
    if not request.is_ajax():
        if request.method != 'POST':
            # respond with error
            return HttpResponse("Request is not valid",
                                content_type="application/json",
                                status=404)

    form = CourseForm(request.POST)
    # fix cleaning, error reporting
    if not form.is_valid() and 0:
        return HttpResponse("Form is invalid",
                            content_type="application/json",
                            status=404)

    course = get_object_or_404(
                Course,
                number=course_number,
                semester=course_semester)

    course.name = form.cleaned_data['name']
    course.number = form.cleaned_data['number']
    course.semester = form.cleaned_data['semester']
    course.max_enroll = form.cleaned_data['max_enroll']
    course.description = form.cleaned_data['description']
    course.access_code = form.cleaned_data['access_code']
    course.public = form.cleaned_data['public']

    course.save()

    json_obj = {"message": "Successfully updated"}

    return HttpResponse(json.dumps(json_obj), content_type='application/json')


@login_required
@transaction.atomic
def add_person_to_course(request):
    if not request.is_ajax():
        if request.method != 'POST':
            # respond with error
            return HttpResponse("Request is not valid", content_type="application/json", status=404)

    course_number = request.POST.get("course_number", "")
    course_semester = request.POST.get("course_semester", "")
    username = request.POST.get("username", "")
    role = request.POST.get("role", "")

    if (course_number == "" or course_semester == "" or
        username == "" or role == ""):
        return HttpResponse("Invalid parameters", content_type="application/json", status=400)

    course = get_object_or_404(Course, number=course_number, semester=course_semester)

    if role == 'instructor':
        group = course.instructors
    elif role == 'staff':
        group = course.staff
    elif role == 'student':
        group = course.students
    else:
        return HttpResponse("Invalid parameters", content_type="application/json", status=400)

    if group.filter(username__exact=username).count() != 0:
        return HttpResponse("Already a member", content_type="application/json", status=400)

    user = get_object_or_404(User, username__exact=username)

    # remove from any other groups the user
    # may have been for the course

    if course.instructors.filter(username__exact=username).count() != 0:
        course.instructors.remove(user)
    if course.staff.filter(username__exact=username).count() != 0:
        course.staff.remove(user)
    if course.students.filter(username__exact=username).count() != 0:
        course.students.remove(user)

    # add the user to their new role
    group.add(user)

    message = ("You have been added to " + course_number + " " + course_semester +
               " as a " + role + ".")

    # TODO: send notifications to user

    json_obj = {
            "first_name":user.first_name,
            "last_name":user.last_name
            }

    return HttpResponse(json.dumps(json_obj), content_type='application/json')



####### For team_create_page #######

## Kaan's part starts here

@login_required
@transaction.atomic
def submit_team(request):
    if not request.is_ajax():
        if request.method != 'POST':
            # respond with error
            return HttpResponse("Request is not valid", content_type="application/json", status=404)

    # TODO: fix error messages
    team_name = request.POST.get("team_name", "")
    team_members = json.loads(request.POST.get("team_members",""))
    assignment_number = request.POST.get("assignment_number", "")
    course_number = request.POST.get("course_number", "")

    if (team_name == "" or team_members == "" or
        course_number == "" or assignment_number == ""):
        return HttpResponse("No team name provided", content_type="application/json", status=400)

    # TODO: race condition in this case
    for member in team_members:
        person = Person.objects.get(user__username=member);
        if person == None:
            return HttpResponse("Team member does not exist", content_type="application/json", status=400)
        teams = person.teams
        if teams != None:
            if teams.filter(assignment__number=assignment_number).count() != 0:
                return HttpResponse("Person is already in a team", content_type="application/json", status=400)

    try:
        course = Course.objects.get(number=course_number)
    except ObjectDoesNotExist:
        return HttpResponse("Course does not exist", content_type="application/json", status=400);

    course_assignments = course.assignments
    try:
        assignment = course_assignments.get(number=assignment_number)
    except ObjectDoesNotExist:
        return HttpResponse("Assignment does not exist", content_type="application/json", status=400)

    team = Team(team_name=team_name, assignment=assignment, members=team_members)
    team.save()


    # TODO: send notifications
    send_notifications(message, '/myteam/'+course_number+'/'+assignment_number+'/', team_members)

    json_obj = {
            "message":"Team "+team_name+" created!"
            }

    return HttpResponse(json.dumps(json_obj), content_type='application/json')

@login_required
def my_team_page(request, course_number, assignment_number):
    context={}

    course = get_object_or_404(Course, number=course_number)
    try:
        assignment = course.assignments.get(number=assignment_number)
    except ObjectDoesNotExist:
        return HttpResponse("Invalid assignment", status=400)

    person = request.user.person
    try:
        team = person.teams.get(assignment_id=assignment.id)
    except ObjectDoesNotExist:
        return HttpResponse("Team does not exist", status=400)


    context['course'] = course
    context['assignment'] = assignment
    context['team_members'] = team.members
    context['team_name'] = team.name

    return render(request, "my_team_page.html", context)

## Kaan's part ends here

####### For administration_page #######


# Mrigesh's part starts here

@login_required
def forum(request, semester_id, course_id):
    # View all posts (within a single course 'c')
    c = Course.objects.filter(semester=semester_id,number=course_id)

    context = {}
    posts = Post.objects.filter(course=c).order_by('-updated_at')
    # TODO : Add filtering based on user visibility of that post
    context = {'posts' : posts }
    filters = [ ('All',24),('Unread',18) ]
    context['filters'] = filters
    context['selected'] = None
    context['following'] = []
    context['course_id'] = course_id
    context['semester_id'] = semester_id
    context['selected_post'] = int(request.GET.get('p',0))

    return render(request, 'forum.html',context)


@login_required
def view_post(request, post_id):
    posts = [Post.objects.get(id=post_id)]
    context = {'posts' : posts }
    return render(request, 'view_post.html',context)

@login_required
@transaction.atomic
def post(request,semester_id,course_id,parent_id):
    form = PostForm()
    context = {'form':form}
    # Create new post
    return render(request, 'post.html',context)

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
def edit_post(request, id):
	# Edit content
	# Change visibility
	# Assign to students
    return

# Mrigesh's part ends here

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


@login_required
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
    return render(request, "home.html", {})

@login_required
def manage_courses(request):
    return render(request, "managecourses.html", {})

## TODO: this currently holds the edit course page,
##       change this to the forum page once it is done
@login_required
def view_course_page(request, number):
    context={}

    try:
        course = Course.objects.get(number=number)
    except ObjectDoesNotExist:
        HttpResponse("Course not found", status=400);

    role = ''

    if course.instructors.filter(username=request.user.username).count() > 0:
        role = "instructor"
    elif course.staff.filter(username=request.user.username).count() > 0:
        role = "staff"
    elif course.students.filter(username=request.user.username).count() > 0:
        role = "student"

    context['role'] = role

    # TODO: change this to the forum page
    if role != '' or course.public:
        return render(request, "edit_course.html",{"course": course})
    else:
        return render(request, "home.html", {"errors": ["Course is not public."]})

@login_required
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
        return render(request, 'course_creation.html')
    form = CourseForm(request.POST)

    if not form.is_valid():
        return render(request, 'course_creation.html', {'form': form})

    course = Course(number=form.cleaned_data['number'],
                    name=form.cleaned_data['name'],
                    semester=form.cleaned_data['semester'],
                    description=form.cleaned_data['description'],
                    max_enroll=form.cleaned_data['max_enroll'],
                    access_code=form.cleaned_data['access_code'],
                    public=form.cleaned_data['public'])

    course.save()

    # add ourselves as the manager of this course
    request.user.courses_managed.add(course)
    course.instructors.add(request.user)

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

