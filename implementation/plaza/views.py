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
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings
from datetime import datetime
from django.utils.html import *
from annoying.functions import get_object_or_None
import pusher

## Role based course/user interaction ##
class Role:
    instructor = 0
    staff = 1
    student = 2
    none = 3

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

### Role/Permission Helper Function ####

def get_user_role(user, course):
    if course.instructors.filter(username=user.username).exists():
        return Role.instructor
    elif course.staff.filter(username=user.username).exists():
        return Role.staff
    elif course.students.filter(username=user.username).exists():
        return Role.student
    else:
        return Role.none

def user_has_permission(user, course, required_role):
    user_role = get_user_role(user, course)
    if required_role == Role.instructor:
        if user_role == Role.instructor:
            return True
    if required_role == Role.staff:
        if (user_role == Role.instructor or
            user_role == Role.staff):
            return True
    if required_role == Role.student:
        if (user_role == Role.instructor or
            user_role == Role.staff or user_role == Role.student):
            return True
    return False

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
    new_person, created = Person.objects.get_or_create(user=new_user, nickname=new_user.username)
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
            return HttpJSONStatus("Request is not valid", status=404)

    course_number = request.POST.get("course_number", "")
    course_semester = request.POST.get("course_semester", "")
    username = request.POST.get("username", "")
    role = request.POST.get("role", "")

    if (course_number == "" or course_semester == "" or
        username == "" or role == ""):
        return HttpJSONStatus("Invalid parameters", status=400)

    course = get_object_or_404(Course, number=course_number, semester=course_semester)


    if role == 'instructor':
        group = course.instructors
        required_role = Role.instructor
    elif role == 'staff':
        group = course.staff
        required_role = Role.instructor
    elif role == 'student':
        required_role = Role.staff
        group = course.students
    else:
        return HttpJSONStatus("Invalid parameters", status=400)

    ## check if user has the required permissions
    if not user_has_permission(request.user, course, required_role):
        return HttpJSONStatus("You don't have permission to remove a person!", status=400)

    # if we are removing an instructor, we need to check
    # that there are more in the course
    if role == 'instructor':
        if course.instructors.count() == 1:
            return HttpJSONStatus("Can't remove last instructor", status=400)

    user = get_object_or_404(User, username__exact=username)

    # remove the person from the group if they exist

    if group.filter(username__exact=username).count() != 0:
        group.remove(user)
    else:
        return HttpJSONStatus("Not a member", status=400)

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
            return HttpJSONStatus("Request is not valid", status=404)

    form = CourseForm(request.POST)
    # fix cleaning, error reporting
    if not form.is_valid():
        return HttpJSONStatus("Form is invalid", status=404)

    course = get_object_or_404(
                Course,
                number=course_number,
                semester=course_semester)

    ## check if user has the required permissions
    if not user_has_permission(request.user, course, Role.instructor):
        return HttpJSONStatus("You don't have permission to edit course!", status=400)


    course.name = form.cleaned_data['name']
    course.max_enroll = form.cleaned_data['max_enroll']
    course.description = form.cleaned_data['description']
    course.access_code = form.cleaned_data['access_code']
    course.public = form.cleaned_data['public']
    course.save()

    return HttpJSONStatus("Successfully updated", status=200)

@login_required
@transaction.atomic
def add_tag_to_course(request):
    if not request.is_ajax():
        if request.method != 'POST':
            return HttpJSONStatus("Request is not valid", status=400)

    course_number = request.POST.get("course_number", "")
    course_semester = request.POST.get("course_semester", "")
    tag_name = request.POST.get("tag_name", "")

    if (course_number == "" or course_semester == "" or
        tag_name == ""):
        return HttpJSONStatus("Invalid parameters", status=400)

    course = get_object_or_404(Course, number=course_number, semester=course_semester)

    ## check if user has the required permissions
    if not user_has_permission(request.user, course, Role.staff):
        return HttpJSONStatus("You don't have permission to add a tag!", status=400)

    if (course.tags.filter(name=tag_name).count() != 0):
        return HttpJSONStatus("Tag with name already exists.", status=400)

    tag = Tag(name=tag_name, course=course)
    tag.save()

    return HttpJSONStatus("Tag "+tag_name+" successfully created!", status=200)



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

    ## check if user has the required permissions
    if not user_has_permission(request.user, course, Role.staff):
        return HttpJSONStatus("You don't have permission to add assignments!", status=400)


    if (course.assignments.filter(title=assignment_title).count() != 0):
        return HttpJSONStatus("Assignment with title already exists.", status=400)

    if (course.assignments.filter(number=assignment_number).count() != 0):
        return HttpJSONStatus("Assignment with number already exists.", status=400)

    assignment = Assignment(title=assignment_title,
                            number=assignment_number,
                            course=course)
    assignment.save()

    # automatically create a tag for assignment
    if course.tags.filter(name=assignment_title).count() == 0:
        tag = Tag(name=assignment_title, course=course)
        tag.save()

    return HttpJSONStatus("Assignment "+assignment_number+" successfully created!", status=200)


@login_required
@transaction.atomic
def remove_tag_from_course(request):
    if not request.is_ajax():
        if request.method != 'POST':
            return HttpJSONStatus("Request is not valid", status=400)

    course_number = request.POST.get("course_number", "")
    course_semester = request.POST.get("course_semester", "")
    tag_name = request.POST.get("tag_name", "")

    if (course_number == "" or course_semester == "" or
        tag_name == ""):
        return HttpJSONStatus("Invalid parameters", status=400)

    course = get_object_or_404(Course, number=course_number, semester=course_semester)

    ## check if user has the required permissions
    if not user_has_permission(request.user, course, Role.staff):
        return HttpJSONStatus("You don't have permission to remove a tag!", status=400)


    tags = course.tags.filter(name=tag_name)
    if tags.count() > 0:
        tags.all()[0].delete()

    return HttpJSONStatus("Tag "+tag_name+" successfully deleted!", status=200)




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

    ## check if user has the required permissions
    if not user_has_permission(request.user, course, Role.staff):
        return HttpJSONStatus("You don't have permission to remove an assignment!", status=400)

    try:
        assignment = course.assignments.get(title=assignment_title)
    except ObjectDoesNotExist:
        return HttpJSONStatus("Assignment doesn not exist", status=400)


    tags = course.tags.filter(name=assignment_title)
    if tags.count() == 1:
        tags.all()[0].delete()
    assignment.delete()

    return HttpJSONStatus("Assignment "+assignment_title+" successfully deleted!", status=200)




@login_required
@transaction.atomic
def add_person_to_course(request):
    if not request.is_ajax():
        if request.method != 'POST':
            # respond with error
            return HttpJSONStatus("Request is not valid", status=404)

    course_number = request.POST.get("course_number", "")
    course_semester = request.POST.get("course_semester", "")
    username = request.POST.get("username", "")
    role = request.POST.get("role", "")

    if (course_number == "" or course_semester == "" or
        username == "" or role == ""):
        return HttpJSONStatus("Invalid parameters", status=400)

    course = get_object_or_404(Course, number=course_number, semester=course_semester)

    if role == 'instructor':
        group = course.instructors
        required_role = Role.instructor
    elif role == 'staff':
        group = course.staff
        required_role = Role.instructor
    elif role == 'student':
        required_role = Role.staff
        group = course.students
    else:
        return HttpJSONStatus("Invalid parameters", status=400)

    ## check if user has the required permissions
    if not user_has_permission(request.user, course, required_role):
        return HttpJSONStatus("You don't have permission to add this person!", status=400)

    if group.filter(username__exact=username).count() != 0:
        return HttpJSONStatus("Already a member", status=400)

    user = get_object_or_404(User, username__exact=username)

    # remove from any other groups the user
    # may have been for the course

    if course.instructors.filter(username__exact=username).count() != 0:
        if not user_has_permission(request.user, course, Role.instructor):
            return HttpJSONStatus("You don't have permission to transfer "+username, status=400)
        if course.instructors.count() == 1:
            return HttpJSONStatus("Can't transfer the last instructor in the course!",status=400)
        course.instructors.remove(user)
    if course.staff.filter(username__exact=username).count() != 0:
        if not user_has_permission(request.user, course, Role.instructor):
            return HttpJSONStatus("You don't have permission to transfer "+username, status=400)
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

    # Check if the user is actually in the team
    if not team.members.filter(person=user.person).exists():
        return HttpJSONStatus("Cannot add a person to a team you're not part of!", status=400)

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

    return HttpResponse(
            json.dumps(user_as_simple_json(user)),
            content_type="application/json",
            status=200)

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

    if request.user.username != username:
        return HttpJSONStatus("You can not remove someone else from a team!", status=400)

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

    try:
        course = Course.objects.get(number=course_number, semester=course_semester)
    except ObjectDoesNotExist:
        return HttpJSONStatus("Course does not exist", status=400)

    # add ourselves to the list
    team_members.append(request.user.username)

    if (team_name == "" or team_members == "" or
        course_number == "" or assignment_number == ""):
        return HttpJSONStatus("No team name provided", status=400)

    # check that every person is a student
    # and not in a team for this assingment
    for member in team_members:
        person = Person.objects.get(user__username=member);

        if get_user_role(person.user, course) != Role.student:
            return HttpJSONStatus("Only students of the class can be in a team!", status=400)

        teams = person.teams
        if teams != None:
            if teams.filter(assignment__number=assignment_number).count() != 0:
                return HttpJSONStatus("Person is already in a team", status=400)

    course_assignments = course.assignments

    try:
        assignment = course_assignments.get(number=assignment_number)
    except ObjectDoesNotExist:
        return HttpJSONStatus("Assignment does not exist", status=400)

    team = Team(name=team_name, assignment=assignment)
    team.save()

    team_post_id = -team.id
    p = Post(title = team.name + ' personal thread', text = 'You can communicate here',author = None, parent_id = team_post_id, root_id = team_post_id, course = course, post_type = 2)
    p.save()

    #add ourselves to the team and then the other members
    for member in team_members:
        team.members.add(get_object_or_404(Person,user__username=member))

    notif_url = "/myteam/"+course_semester+"/"+course_number+"/"+assignment_number
    save_and_notify('8', person, target_user.person, '', "/profile/"+str(request.user.id))

    return HttpJSONStatus("Team "+team_name+" created!", status=200)

@login_required
def my_team_page(request, course_number, course_semester, assignment_number):
    context={}

    course = get_object_or_404(Course, number=course_number, semester=course_semester)
    try:
        assignment = course.assignments.get(number=assignment_number)
    except ObjectDoesNotExist:
        return HttpJSONStatus("Invalid assignment", status=400)

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
    context['post_id'] = -int(team.id)

    return render(request, "my_team_page.html", context)

## Kaan's part ends here

####### For administration_page #######


# Mrigesh's part starts here

@login_required
def forum(request, semester_id, course_id):
    # View all posts (within a single course 'c')
    c = Course.objects.get(semester=semester_id,number=course_id)

    if not user_has_permission(request.user, c, Role.student):
        return redirect('coursesignup', c.semester, c.number)

    posts = Post.objects.filter(course=c).filter(parent_id=0).order_by('-updated_at')

    q = request.GET.get('q', '')
    for search_term in q.split():
      posts=posts.filter(Q(title__icontains = search_term) | Q(text__icontains = search_term))


    context = {'posts' : posts }
    filters = [ ('All',len(posts)),('Unread',18) ]
    context['filters'] = filters
    context['search_term'] = q
    context['selected'] = None
    context['following'] = []
    context['course_id'] = course_id
    context['semester_id'] = semester_id
    context['selected_post'] = int(request.GET.get('p',0))

    return render(request, 'forum.html',context)


@login_required
def forum_home(request, semester_id, course_id):
    c = Course.objects.get(semester=semester_id,number=course_id)

    if not user_has_permission(request.user, c, Role.student):
        return redirect('coursesignup', c.semester, c.number)

    context = {}
    context['course_id'] = course_id
    context['semester_id'] = semester_id


    return render(request, 'forum_home.html',context)

@login_required
def view_post(request, post_id):
  if int(post_id) > 0:
    p = Post.objects.get(id=post_id)
    root_id = p.id if p.root_id == 0 else p.root_id
    posts = [Post.objects.get(id=root_id)]

  elif int(post_id) < 0:
    p = Post.objects.get(parent_id=post_id)
    posts = [p]
    root_id = p.id

  if not user_has_permission(request.user, p.course, Role.student):
    return redirect('coursesignup', c.semester, c.number)

  posts += Post.objects.filter(root_id=p.id)

  context = {'posts' : posts }
  context['form'] = PostForm()
  context['root_id'] = int(root_id)
  context['course_id'] = int(p.course.number)
  context['semester_id'] = p.course.semester
  return render(request, 'view_post.html',context)


@login_required
@transaction.atomic
def post(request,semester_id,course_id,parent_id):
  if request.method == 'POST':
    form = PostForm(request.POST)
    context = {'form':form}
    if form.is_valid():
      c = Course.objects.get(semester=semester_id,number=course_id)

      if not user_has_permission(request.user, c, Role.student):
        return redirect('coursesignup', c.semester, c.number)

      author = Person.objects.get(user=request.user)
      # TODO : Check if author can post in this course

      parent_post = None
      root_post   = None

      if str(parent_id) <> '0':
        parent_post = Post.objects.get(id=parent_id)
        root_post   = parent_post
        while int(parent_post.parent_id) > 0:
          root_post = Post.objects.get(id=root_post.parent_id)

      p = Post(title      = form.cleaned_data['title'],
               text       = form.cleaned_data['text'],
               author     = author,
               parent_id  = parent_id,
               root_id    = root_post.id if root_post is not None else 0,
               course     = c,
               post_type  = form.cleaned_data['post_type'],
               )

      p.save()

      if str(p.post_type[0]) == '0':
        q = Post(title = 'student answer', text = 'Students, please use this space to answer the question', author = None, parent_id = p.id, root_id = p.id, course = c, post_type = 1)
        q.save()

        s = Post(title = 'staff answer', text = 'The staff will answer here', author = None, parent_id = p.id, root_id = p.id, course = c, post_type = 2)
        s.save()

      return redirect('view_post',(p.root_id if p.root_id <> 0 else p.id))
    else:
      print form.errors

  else:
    form = PostForm()

  context = {'form':form}
  c = Course.objects.get(semester=semester_id,number=course_id)
  context['course_id'] = course_id
  context['semester_id'] = semester_id
  context['tags']=c.tags.all()
  context['types'] = [('3','Comment')]
  if str(parent_id) == '0' and request.user in c.students.all():
    context['types'].insert(0,('0','Question') )

  return render(request, 'post.html',context)


@login_required
@transaction.atomic
def edit_post(request,post_id):
  if request.method == 'POST':
    # TODO: VALIDATE
    #if not user_has_permission(request.user, c, Role.student):
    #    return redirect('coursesignup', c.semester, c.number)

      author = request.user.person
      # TODO : Check if author can post in this course
      p = Post.objects.get(id=post_id)
      if p.author == author:
        p.text = request.POST.get('text')
        p.save()

      return redirect('view_post',(p.root_id if p.root_id <> 0 else p.id))

  return(redirect('view_post',post_id))



@login_required
@transaction.atomic
def delete_post(request, id):
    # Delete a post
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
def follow_tag(request):
	# Follow a specific tag
    return

@login_required
@transaction.atomic
def unfollow_tag(request):
    # unfollow a specific tag
    return

@login_required
def get_new_posts_json(request,semester_id,course_id,post_id):
    response_text = ''
    p = get_object_or_None(Post,id=post_id)
    c = Course.objects.get(number=course_id,semester=semester_id)
    if p is None and int(post_id) > 0:
      return HttpResponse('[]', content_type="application/json")

    posts = Post.objects.filter(course=c).filter(parent_id=0,id__gt=post_id).order_by('updated_at')
    for post in posts:
      response_text +=  '{"post_id":'+str(post.id)
      response_text +=  ', "title":"'+escape(str(post.title))+'"'
      response_text +=  ', "text":"'+escape(strip_tags(str(post.text)))[:66]+'"'
      response_text +=  ', "timestamp":"'+post.updated_at.strftime('%b %d, %H:%M') +'"'
      response_text +=  '},\n'

    
    response_text = '[' + response_text[:-2] + ']'
    return HttpResponse(response_text, content_type="application/json")

####### For ajax  #######
# Mrigesh's part ends here


@login_required
def search_student(request):
    if not request.is_ajax():
        if request.method != 'POST':
            # respond with error
            return HttpJSONStatus("Request is not valid", status=404)


    username = request.POST.get("username","")

    if username == "":
        return HttpJSONStatus("Username not provided", status=404)

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
@transaction.atomic
def edit_course(request, course_semester, course_number):
    context={}

    try:
        course = Course.objects.get(number=course_number)
    except ObjectDoesNotExist:
        HttpResponse("Course not found", status=400);

    role = ''

    if not user_has_permission(request.user, course, Role.staff):
        return redirect('home_msg',"","You do not have permission to view this course!")

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

pusher_client = pusher.Pusher(
  app_id='199771',
  key='692221dea02c47027435',
  secret='3f8f9ff3b6fb3008becf',
  ssl=True
)

# @login_required
@transaction.atomic
def follow_user(request, id):
    person = request.user.person
    target_user = User.objects.get(id=id)
    person.following.add(target_user)
    save_and_notify('7', person, target_user.person, '', "/profile/"+str(request.user.id))
    return redirect(reverse('profile', kwargs={'id': id}))

# @login_required
@transaction.atomic
def unfollow_user(request,id):
    person = request.user.person
    target_user = User.objects.get(id=id)
    # person.following.add(target_user)
    person.following.remove(target_user)
    return redirect(reverse('profile', kwargs={'id': id}))

# @login_required
def get_profile_picture(request, id):
    person = get_object_or_404(Person,user_id=id)
    if not person.profile_image:
        raise Http404
    content_type = guess_type(person.profile_image.name)
    return HttpResponse(person.profile_image, content_type=content_type)

# General notification API
def save_and_notify(action, sender, receiver, extra_content, destination):
    notification = Notification(action=action, sender=sender, receiver=receiver, extra_content=extra_content, destination=destination)
    notification.save()
    pusher_client.trigger('noti_channel', 'my_event', {'message': 'New Notification!'})
    return

# @login_required
def get_notification(request, id):
    unread_notis = Notification.objects.filter(status='0', receiver__user__id=id).order_by('-created_at')[:5]
    json = []
    for n in unread_notis:
        noti_json = {
            "sender": n.sender.user.username,
            "sender_id": n.sender.user.id,
            "action": n.get_action_display(),
            "extra_content": n.extra_content,
            "created_at": n.created_at.strftime("%b %d, %H:%M:%S"),
            "destination": n.destination
        }
        json.append(noti_json)
    return JsonResponse(json, safe=False)

def mark_as_read(request, id):
    notification = Notification.objects.filter(id=id).update(status='1')
    return redirect(reverse('notification'))

def unread_number(request):
    count = Notification.objects.filter(receiver__user__id=request.user.id, status='0').count()
    return JsonResponse({'un':count}, safe=False)

# Change password
# @login_required
def change_password(request):
    errors = []
    context = {}
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=request.user.username,password=data['opassword'])
            if user is not None:
                newuser = User.objects.get(username__exact=request.user.username)
                newuser.set_password(data['npassword1'])
                newuser.save()
                return redirect(reverse('login'))
            else:
                errors.append('Old password is not correct')
        print form.errors
        context['errors'] = errors
        context['form'] = form
    return render(request, "account.html", context)

############################################## Display pages #############################################


@login_required
def home_page(request):
    # With different users, display either home/staff home page
    context = {'c_student'  : request.user.courses_taken.all()}
    context['c_staff']      = request.user.courses_assisted.all()
    context['c_instructor'] = request.user.courses_managed.all()
    return render(request, "home.html", context)

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
    user = User.objects.get(id=id)
    context["person"] = user.person
    context["request_id"] = request.user.id
    if user in request.user.person.following.all():
        context['following'] = 'Yes'
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

@login_required
@transaction.atomic
def course_signup_page(request, course_semester, course_number):
    course = get_object_or_404(Course, number=course_number, semester=course_semester)
    errors=[]
    context = {"course": course, "errors":errors}
    if get_user_role(request.user, course) != Role.none:
        redirect('forum',course_semester,course_number)
    if request.method == "GET":
        return render(request, "course_signup.html", context)
    if request.method == "POST":
        form = CourseSignupForm(request.POST)
        if not course.public:
            if not form.is_valid():
                errors.append("Enter an access code")
                return render(request, "course_signup.html",context)
            if form.cleaned_data['access_code'] != course.access_code:
                errors.append("The access code you entered was not valid!")
                return render(request, "course_signup.html", context)

        course.students.add(request.user)
        return redirect('forum', course_semester, course_number)


@login_required
@transaction.atomic
def course_creation_page(request):
	# Show the page to create courses
	# This is only accessible by staffs (actuallt it could be integrated into administration page as a dropdown panel)
    context = {}
    if request.method == 'GET':
        return render(request, 'course_creation.html')
    form = CourseForm(request.POST)

    if not form.is_valid():
        return render(request, 'course_creation.html', {'form': form})

    if Course.objects.filter(number=form.cleaned_data['number'],
                             semester=form.cleaned_data['semester']).exists():
        return render(request,
                      "course_creation.html",
                      {"form":form, "errors":["Course already exists!"]})

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
    try:
        course = Course.objects.get(
                semester=course_semester,
                number=course_number)
        assignment = Course.assignments.get(number=assignment_number)
    except ObjectDoesNotExist:
        return redirect('home_msg', '', 'Invalid team page!')

    if user_get_permission(request.user, course) != Role.student:
        return redirect('home_msg', '', 'You are not a student of this course!')

    context = {
            "course_number": course_number,
            "course_semester": course_semester,
            "assignment_number":assignment_number
            }

    return render(request, "team_creation.html", context)

def resource_page(request, semester_id, course_id, id):
	# Show the page of resources (notes, videos)
	# For staff, there's an optiona for uploading new resources
    context = {}
    context['sid'] = semester_id
    context['cid'] = course_id
    if id != '0':
        context['parent'] = Resource.objects.get(id=id)
    context['parent_rid'] = id
    context['resource_file_form'] = ResourceFileForm()
    context['resource_folder_form'] = ResourceFolderForm()
    if id == '0':
        c = Course.objects.get(semester=semester_id,number=course_id)
        resources = Resource.objects.filter(parent=None, course=c)
        context['resources'] = resources
    else:
        resources = Resource.objects.get(id=id).children.all()
        context['resources'] = resources
    return render(request, "resources.html", context)

def create_resource(request, semester_id, course_id, id):
    rtype = request.POST.get('rtype', False)
    c = Course.objects.get(semester=semester_id,number=course_id)
    parent = None
    if id != '0':
        parent = Resource.objects.get(id=id)
    if rtype == "folder":
        resource = Resource(resource_type='F', parent=parent, course=c)
        resource_folder_form = ResourceFolderForm(request.POST, instance=resource)
        resource_folder_form.save()
    if rtype == "file":
        resource = Resource(resource_type='P', parent=parent, course=c)
        resource_file_form = ResourceFileForm(request.POST, request.FILES, instance=resource)
        if not resource_file_form.is_valid():
            errors = json.dumps([{'errors': True}, resource_file_form.errors])
            return HttpResponse(errors, content_type='application/json')
        resource_file_form.save()
    return redirect(reverse('resource', kwargs={'semester_id':semester_id, 'course_id':course_id, 'id':id}))

def delete_resource(request, semester_id, course_id, id):
    print id, "fuck"
    parent = Resource.objects.get(id=id).parent
    pid = 0
    if parent:
        pid = parent.id
    resource = Resource.objects.filter(id=id)
    resource.delete()
    return redirect(reverse('resource', kwargs={'semester_id':semester_id, 'course_id':course_id, 'id':pid}))


def resource_parent(request, semester_id, course_id, id):
    if id == '0':
        return redirect(reverse('resource', kwargs={'semester_id':semester_id, 'course_id':course_id, 'id':id}))
    parent = Resource.objects.get(id=id).parent
    pid = 0
    if parent:
        pid = parent.id
    return redirect(reverse('resource', kwargs={'semester_id':semester_id, 'course_id':course_id, 'id':pid}))



# @login_required
def resource_slide_page(request):
	# Show the page a slide (could be a pdf slide, or just streaming the video)
	# Students could post comments to each slide / video
	return

def notification_page(request):
    context = {}
    context['notifications'] = Notification.objects.filter(receiver__user__id=request.user.id)
    return render(request, "notification.html", context)


## Dynamic Object Suggestion ##
def course_num_suggestions(input_data):
    courses = Course.objects.filter(number__startswith=input_data)[:10].all()
    serialized_courses = serializers.serialize("json",courses)
    return serialized_courses

def user_as_simple_json(user):
    return dict(username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                user_id=user.id)

def username_suggestions(input_data):
    users = User.objects.filter(username__startswith=input_data).all()
    simplified = [user_as_simple_json(usr) for usr in users]
    serialized_users = json.dumps(simplified)
    return serialized_users

def username_in_course_suggestions(input_data, course_semester, course_number):
    course = get_object_or_404(Course, semester=course_semester, number=course_number);
    users = course.students.filter(username__startswith=input_data).all()
    simplified = [user_as_simple_json(usr) for usr in users]
    serialized_users = json.dumps(simplified)
    return serialized_users

@login_required
def dynamic_obj_suggestion(request):
    if not request.is_ajax():
        if request.method != 'POST':
            return HttpJSONStatus("Request is not valid",status=400)

    input_type = request.POST.get("input_type", "")
    input_data = request.POST.get("input_data", "")

    if input_type == "":
        return HttpJSONStatus("Invalid parameters", status=400)

    if input_data =="":
        return HttpResponse(json.dumps(None), content_type='application/json')

    # find any suggestions on the object based on the type
    if input_type == "course_number":
        suggestions = course_num_suggestions(input_data)
    elif input_type == "username":
        course_number = request.POST.get("course_number", "")
        course_semester = request.POST.get("course_semester", "")
        if course_number == "" or course_semester == "":
            suggestions = username_suggestions(input_data)
        else:
            suggestions = username_in_course_suggestions(input_data, course_semester, course_number)
    else:
        return HttpJSONStatus("Unsupported input type!", status=400)

    return HttpResponse(suggestions, content_type='application/json')

@login_required
def account_page(request):
    context = {}
    return render(request, "account.html", context)
