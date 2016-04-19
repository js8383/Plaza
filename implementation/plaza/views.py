import json

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
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
from mimetypes import guess_type

from django.conf import settings


# Create your views here.

############################################## Functionality #############################################

###### AJAX Helper Functions #######

# used in sending status/error messages back
# to the client
def HttpJSONStatus(msg,status):

    json_obj = {"message":msg}

    return HttpResponse(json.dumps(json_obj),
                        content_type='application/json',
                        status=status)

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

    # Create a default user profile image
    # profile_image_url = settings.MEDIA_ROOT + "profile-photos/user_ico_" + str(new_user.id)


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
    if not form.is_valid():
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
def add_assignment_to_course(request):
    if not request.is_ajax():
        if request.method != 'POST':
            # respond with error
            return HttpJSONStatus("Request is not valid", status=400)

    course_number = request.POST.get("course_number", "")
    course_semester = request.POST.get("course_semester", "")
    assignment_title = request.POST.get("assignment_title", "")
    assignment_number = request.POST.get("assignment_number", "")

    if (course_number == "" or course_semester == "" or
        assignment_title == "" or assignment_number == ""):
        return HttpJSONStatus("Invalid parameters", status=400)

    course = get_object_or_404(Course, number=course_number, semester=course_semester)


    if (course.assignments.filter(title=assignment_title).count() != 0):
        return HttpJSONStatus("Assignment with title already exists.", status=400)

    if (course.assignments.filter(number=assignment_number).count() != 0):
        return HttpJSONStatus("Assignment with number already exists.", status=400)

    assignment = Assignment(title=assignment_title,
                            number=assignment_number,
                            course=course)
    assignment.save()

    return HttpJSONStatus("Assignment "+assignment_number+" successfully created!", status=200)

@login_required
@transaction.atomic
def remove_assignment_from_course(request):
    if not request.is_ajax():
        if request.method != 'POST':
            # respond with error
            return HttpJSONStatus("Request is not valid", status=400)

    course_number = request.POST.get("course_number", "")
    course_semester = request.POST.get("course_semester", "")
    assignment_title = request.POST.get("assignment_title", "")

    if (course_number == "" or course_semester == "" or
        assignment_title == ""):
        return HttpJSONStatus("Invalid parameters", status=400)

    course = get_object_or_404(Course, number=course_number, semester=course_semester)

    try:
        assignment = course.assignments.get(title=assignment_title)
    except ObjectDoesNotExist:
        return HttpJSONStatus("Assignment doesn not exist", status=400)

    assignment.delete()

    return HttpJSONStatus("Assignment "+assignment_title+" successfully deleted!", status=200)




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
def add_person_to_team(request):
    if not request.is_ajax():
        if request.method != 'POST':
            # respond with error
            return HttpJSONStatus("Request is not valid", status=404)

    username = request.POST.get("username", "")
    team_id = request.POST.get("team_id", "")

    if username == "" or team_id == "":
        return HttpJSONStatus("Invalid request parameters", status=400)

    try:
        team = Team.objects.get(id=team_id)
    except ObjectDoesNotExist:
        return HttpJSONStatus("Team does not exist!", status=400)

    assignment = team.assignment
    if assignment == None:
        return HttpJSONStatus("Team does not have an assignment!", status=400)

    try:
        user = User.objects.get(username__exact=username)
    except ObjectDoesNotExist:
        return HttpJSONStatus("User does not exist!", status=400)

    if user.person.teams.filter(assignment__id=assignment.id).count() == 1:
        return HttpJSONStatus(username+" already has a team for this assignment!", status=400)

    team.members.add(user.person)
    team.save()

    return HttpJSONStatus("Added " +username+ " to team!", status=200)

@login_required
@transaction.atomic
def remove_person_from_team(request):
    if not request.is_ajax():
        if request.method != 'POST':
            # respond with error
            return HttpJSONStatus("Request is not valid", status=404)

    username = request.POST.get("username", "")
    team_id = request.POST.get("team_id", "")

    if username == "" or team_id == "":
        return HttpJSONStatus("Invalid request parameters", status=400)

    try:
        team = Team.objects.get(id=team_id)
    except ObjectDoesNotExist:
        return HttpJSONStatus("Team does not exist!", status=400)

    try:
        user = User.objects.get(username__exact=username)
    except ObjectDoesNotExist:
        return HttpJSONStatus("User does not exist!", status=400)

    # remove ourselves from the team
    team.members.remove(user.person)
    # if we were the last person
    # delete this team
    if team.members.count() == 0:
        team.delete()

    obj = {"url":"You have successfully left the team!/"}

    return HttpResponse(json.dumps(obj), content_type="application/json", status=200)

@login_required
@transaction.atomic
def submit_team(request):
    if not request.is_ajax():
        if request.method != 'POST':
            return HttpJSONStatus("Request is not valid", status=404)

    team_name = request.POST.get("team_name", "")
    team_members = json.loads(request.POST.get("team_members",""))
    assignment_number = request.POST.get("assignment_number", "")
    course_number = request.POST.get("course_number", "")
    course_semester = request.POST.get("course_semester", "")

    # add ourselves to the list
    team_members.append(request.user.username)

    if (team_name == "" or team_members == "" or
        course_number == "" or assignment_number == ""):
        return HttpJSONStatus("No team name provided", status=400)

    for member in team_members:
        person = Person.objects.get(user__username=member);
        teams = person.teams
        if teams != None:
            if teams.filter(assignment__number=assignment_number).count() != 0:
                return HttpJSONStatus("Person is already in a team", status=400)
    try:
        course = Course.objects.get(number=course_number, semester=course_semester)
    except ObjectDoesNotExist:
        return HttpJSONStatus("Course does not exist", status=400);

    course_assignments = course.assignments

    try:
        assignment = course_assignments.get(number=assignment_number)
    except ObjectDoesNotExist:
        return HttpJSONStatus("Assignment does not exist", status=400)

    team = Team(name=team_name, assignment=assignment)
    team.save()

    #add ourselves to the team and then the other members
    for member in team_members:
        team.members.add(get_object_or_404(Person,user__username=member))

    return HttpJSONStatus("Team "+team_name+" created!", status=200)

@login_required
def my_team_page(request, course_number, course_semester, assignment_number):
    context={}

    course = get_object_or_404(Course, number=course_number, semester=course_semester)
    try:
        assignment = course.assignments.get(number=assignment_number)
    except ObjectDoesNotExist:
        return HttpResponse("Invalid assignment", status=400)

    person = request.user.person
    try:
        team = person.teams.get(assignment_id=assignment.id)
    except ObjectDoesNotExist:
        return redirect(
                'createteam',
                course_semester=course_semester,
                course_number=course_number,
                assignment_number=assignment_number)

    context['course'] = course
    context['assignment'] = assignment
    context['team_members'] = team.members
    context['team_name'] = team.name
    context['team_id'] = team.id

    return render(request, "my_team_page.html", context)

## Kaan's part ends here

####### For administration_page #######


# Mrigesh's part starts here

@login_required
def forum(request, semester_id, course_id):
    # View all posts (within a single course 'c')
    c = Course.objects.get(semester=semester_id,number=course_id)
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
def forum_home(request, semester_id, course_id):
    c = Course.objects.get(semester=semester_id,number=course_id)
    context = {}
    context['course_id'] = course_id
    context['semester_id'] = semester_id

    return render(request, 'forum_home.html',context)

@login_required
def view_post(request, post_id):
    posts = [Post.objects.get(id=post_id)]
    context = {'posts' : posts }
    return render(request, 'view_post.html',context)

@login_required
@transaction.atomic
def post(request,semester_id,course_id,parent_id):
  if request.method == 'POST':
    form = PostForm(request.POST)
    print request.POST
    context = {'form':form}
    if form.is_valid():
      c = Course.objects.get(semester=semester_id,number=course_id)
      author = Person.objects.get(user=request.user)
      # TODO : Check if author can post in this course

      parent_post = None
      root_post   = None

      if str(parent_id) <> '0':
        parent_post = Post.objects.get(id=parent_id)
        root_post   = parent_post
        while parent_post.parent_id is not None:
          root_post = Post.objects.get(id=root_post.parent_id)

      p = Post(title      = form.cleaned_data['title'],
               text       = form.cleaned_data['text'],
               author     = author,
               parent_id  = parent_post,
               root_id    = parent_post,
               course     = c,
               visibility = form.cleaned_data['visibility'],
               post_type  = form.cleaned_data['post_type'],
               )


      p.save()

      return view_post(request,p.id)

  else:
    form = PostForm()

  context = {'form':form}
  c = Course.objects.get(semester=semester_id,number=course_id)
  context['course_id'] = course_id
  context['semester_id'] = semester_id
  context['tags']=c.tags.all()
  if str(parent_id) == '0':
    context['vis'] = [('0','Use my name: ' + request.user.first_name),('1','Anonymous to other students'),('2','Anonymous to all')]
  if str(parent_id) == '0':
    context['types'] = [('0','Question'),('3','Comment')]
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
def upvote(request,post_id):
    # Upvote a post
    return

@login_required
@transaction.atomic
def downvote(request,post_id):
    # Downvote a post
    return

@login_required
@transaction.atomic
def edit_post(request, post_id):
	# Edit content
	# Change visibility
	# Assign to students
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
# Mrigesh's part ends here

def get_notification(request):
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
def edit_course(request, course_semester, course_number):
    context={}

    try:
        course = Course.objects.get(number=course_number)
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
    if role == "staff" or role == "instructor":
        return render(request, "edit_course.html",{"course": course, "role":role})
    else:
        return render(request, "home.html", {"errors": ["Course is not public."]})

    return

@login_required
def search(request):
	# Search for keywords, time, tags
	# Popup (modal in bootstrap) previous posts before someone wants to ask questions contains some similar content
	return

# More to be added

# All notifications stuff and resources and etc.

# General notification API
def save_and_notify(nfilter, sender, receiver, action, target):
    if nfilter == "People":
        if action == "FOLLOW":
            notification = Notification(sender=sender, receiver=receiver, action=action, target_text="you")
            notification.save()
            # notify the leancloud api
    return

# @login_required
@transaction.atomic
def follow_user(request, id):
    user = request.user
    save_and_notify("People", user, user, "FOLLOW", "")
    return

# @login_required
@transaction.atomic
def unfollow_user(request,id):
    return

# @login_required
def get_profile_picture(request, id):
    person = get_object_or_404(Person,user_id=id)
    if not person.profile_image:
        raise Http404
    content_type = guess_type(person.profile_image.name)
    return HttpResponse(person.profile_image, content_type=content_type)

############################################## Display pages #############################################


@login_required
def home_page(request):
    # With different users, display either home/staff home page
    return render(request, "home.html", {})

# Used when we want to redirect users
# back to the home page with a status/err
# message. (course left etc.)
@login_required
def home_page_with_msg(request, status, error):
    statuses = []
    errors = []

    if status != "":
        statuses.append(status)
    if error != "":
        errors.append(error)

    # With different users, display either home/staff home page
    return render(
            request,
            "home.html",
            {"statuses":statuses, "errors":errors})


@login_required
def manage_courses(request):
    return render(request, "managecourses.html", {})

@login_required
def staffhome_page(request, id):
    # With different users, display either home/staff home page
    return render(request, "staff_home.html",{})

# @login_required
def profile_page(request, id):
    context = {}
    context["person"] = request.user.person
    context["target_id"] = id
    return render(request, "profile.html", context)

# @login_required
def edit_profile_page(request):
    user = request.user
    context = {}
    context['person'] = user.person
    if request.method == 'GET':
        return render(request, "profile_edit.html", context)
    form = PersonForm(request.POST, request.FILES)
    # print request.POST["date_of_birth"]

    form.is_valid()
        # return render(request, "profile_edit.html", context)
    form.save(user=user, person=user.person)
    context['form'] = form
    update_session_auth_hash(request, user)
    return render(request, "profile_edit.html", context)

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
def team_creation_page(request, course_number, course_semester, assignment_number):

    # if we already have a team for this assignment
    if (request.user.person.teams.filter(
                assignment__number=assignment_number,
                assignment__course__number=course_number,
                assignment__course__semester=course_semester).count() == 1):
        return redirect(
                'myteamview',
                course_semester=course_semester,
                course_number=course_number,
                assignment_number=assignment_number)

    context = {
            "course_number": course_number,
            "course_semester": course_semester,
            "assignment_number":assignment_number
            }
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

def notification_page(request):
    return render(request, "notification.html", {})
