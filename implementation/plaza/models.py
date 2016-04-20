from __future__ import unicode_literals
from tinymce.models import HTMLField

from django.contrib.auth.models import User
from django.db import models
from datetime import datetime,date
from time import time


def profile_image_rename(instance, filename):
    st = datetime.fromtimestamp(time()).strftime('%Y_%m_%d_%H_%M_%S')
    return 'profile-photos/'+'user_{0}_{1}.'.format(instance.user.id, st)  + filename.split('.')[-1]

class Person(models.Model):
    # Default User fields = username, first_name, last_name, email, password, last_login, date_joined
    user = models.OneToOneField(User,related_name='person') # Enforce andrew_id
    nickname = models.CharField(max_length=32)
    short_bio = models.CharField(max_length=1024, null=True, blank=True)
    date_of_birth = models.DateField(null=True)
    GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'), ('N', 'N/A'))
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    field = models.CharField(max_length=32)
    institution = models.CharField(max_length=32)
    profile_image = models.ImageField(upload_to=profile_image_rename, blank = True, default = 'profile-photos/user_ico.png')
    following = models.ManyToManyField(User, related_name='follows')
    updated_at = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.user.username
    def __str__(self):
        return self.__unicode__()


class Course(models.Model):
    number = models.CharField(max_length=10)
    name = models.CharField(max_length=128)
    semester = models.CharField(max_length=3) # TODO : Create choices of terms and intfield for year
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(null=True) # TODO : validate based on semester/year
    end_time = models.DateTimeField(null=True) # TODO : validate based on semester/year
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    max_enroll = models.IntegerField(null=True)
    access_code = models.IntegerField(null=True)
    public = models.BooleanField(default=True)

    # TODO: Possibly move to a permission-based model instead of rule-based (last sprint)
    students = models.ManyToManyField(User, related_name='courses_taken')
    staff = models.ManyToManyField(User, related_name='courses_assisted')
    instructors = models.ManyToManyField(User, related_name='courses_managed')

    def __unicode__(self):
        return self.semester+'. '+self.name
    def __str__(self):
        return self.__unicode__()


class Tag(models.Model):
    name = models.CharField(max_length=16)
    course = models.ForeignKey(Course, related_name='tags')
    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.__unicode__()


class Post(models.Model):
    title = models.CharField(max_length=128)
    text = HTMLField()
    author = models.ForeignKey(Person,related_name='posts',null=True)
    parent_id = models.IntegerField(default=0)
    root_id = models.IntegerField(default=0)
    course = models.ForeignKey(Course, related_name='posts')

    POST_CHOICES = (('0', 'question'),('1', 'student_reply'),('2', 'staff_reply'),('3', 'comments'))
    post_type = models.CharField(max_length=1, choices=POST_CHOICES,  default='0')

    STATUS_CHOICES = (('0', 'resolved'),('1', 'unresolved'),('2', 'answered'),('3', 'unanswered'))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES,  default='0')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    upvotes = models.IntegerField(default=0) #Duplicate upvotes?
    downvotes = models.IntegerField(default=0)

    assignee = models.OneToOneField(User, related_name="assigned_posts", null=True)
    editors = models.ManyToManyField(User, related_name="edited_posts")
    followers = models.ManyToManyField(User, related_name="followed_posts")
    readers = models.ManyToManyField(User, related_name="read_posts")

    pinned = models.BooleanField(default=False)

    tags = models.ManyToManyField(Tag, related_name='tag_posts')

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.__unicode__()

class Item(models.Model):
    title = models.CharField(max_length=128)
    post = models.ForeignKey(Post, related_name="item")
    owner = models.ForeignKey(Person,related_name='uploads')

    CATEGORY_CHOICES = (('PDF', 'application/pdf'),('JPEG', 'image/jpeg'),('GIF', 'image/gif'),('MP4', 'video/mp4'),('EMBED','text/html'),('PNG','image/png'),('CAL','text/calendar'))
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES,  default='0')

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.__unicode__()


class Assignment(models.Model):
    title = models.CharField(max_length=128)
    number = models.IntegerField(default=0)
    course = models.ForeignKey(Course, related_name='assignments')
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='tag_assignments')
    team_min_size = models.IntegerField(default=1)
    team_max_size = models.IntegerField(default=1)

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.__unicode__()


class Resource(models.Model):
    # course = models.ForeignKey(Course, related_name='resources')
    title = models.CharField(max_length=128)
    notes = models.CharField(max_length=128)
    RTYPE_CHOICES = (('P', 'Plain'), ('D', 'Document'), ('V', 'Video'), ('F', 'Folder'),('N', 'N/A'))
    resource_type = models.CharField(max_length=16, choices=RTYPE_CHOICES)
    due = models.DateField(null=True)
    file = models.FileField(upload_to='resources/')
    # comments = models.ForeignKey(Post,related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='tag_resources')
    parent = models.ForeignKey('self', related_name='children', null=True)

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.__unicode__()

    @property
    def is_past_due(self):
        if date.today() > self.due:
            return True
        return False

    @property
    def get_path(self):
        result = "/" + self.title + "/"
        p = self.parent
        while p != None:
            result = "/" + p.title + result
            p = p.parent
        return result


# Modified by Jason
class Notification(models.Model):
    # course = models.ForeignKey(Course)
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(Person, related_name='notifications_sent')
    receiver = models.ForeignKey(Person, related_name='notifications_received')
    ACTON_CHOICES = (('0', " answered your question"), ('1', " followed your question"), ('2', " commented your question"), ('3', " upvoted your answer"),
                     ('4', " downvoted your answer"), ('5', " replied to your comments"), ('6'," posted a new question in your following tag"), ('7', " followed you"), ('8', " add you to a team"))
    action = models.CharField(max_length=1, choices=ACTON_CHOICES) 
    extra_content = models.CharField(max_length=256)
    STATUS_CHOICES = (('0', 'unseen'),('1', 'seen'))
    status =  models.CharField(max_length=1, choices=STATUS_CHOICES,  default='0')
    destination = models.URLField(max_length=256)

    def __unicode__(self):
        return self.sender.user.username + self.get_action_display()
    def __str__(self):
        return self.__unicode__()


class Team(models.Model):
    name = models.CharField(max_length=128)
    assignment = models.ForeignKey(Assignment, related_name='teams')
    members = models.ManyToManyField(Person, related_name='teams')

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.__unicode__()

class MatchMakingPerson(models.Model):
    person = models.OneToOneField(Person, related_name='matchmaking_person')
    potential_teams = models.ManyToManyField('MatchMakingTeam', related_name='matchmaking_person')
    confirmed_team = models.OneToOneField('MatchMakingTeam', related_name='confirmed_person')

class MatchMakingTeam(models.Model):
    potential_members = models.ManyToManyField(MatchMakingPerson, related_name='potential_team')
    assignment = models.ForeignKey(Assignment, related_name='potential_team')

# TODO: Create settings model object

# TODO: Track views per user per course

# TODO: Create Event model for logs

