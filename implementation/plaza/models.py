from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# Create your models here.

class Tweet(models.Model):
    created_by  = models.ForeignKey(User, related_name="tweet_creator")
    tweet = models.CharField(blank=False, max_length=160)
    creation_time = models.DateTimeField()
    creation_time_string = models.CharField(blank=False,max_length=50)
    # This field is mainly for filter and search
    uname = models.CharField(blank=False, max_length=160)
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="user_profile")
    short_bio = models.CharField(max_length=430, default="No Bio Now")
    age = models.CharField(max_length=3, default="")
    picture = models.FileField(upload_to="pictures", blank=True)
    following = models.ManyToManyField('self', related_name='following_user_profiles')


class Comment(models.Model):
    created_by  = models.ForeignKey(User, related_name="comment_creator")
    original_post = models.ForeignKey(Tweet, related_name="post_under")
    comment = models.CharField(default="", max_length=160)
    creation_time = models.DateTimeField()
    creation_time_string = models.CharField(blank=False,max_length=50)
    # This field is mainly for updateing comment (otherwise missing username)
    uname = models.CharField(blank=False, max_length=160)

class Person(models.Model):
    # Default User fields = username, first_name, last_name, email, password, last_login, date_joined
    user = models.OneToOneField(User) # Enforce andrew_id
    nickname = models.CharField(max_length=32)
    short_bio = models.CharField(max_length=1024, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile-photos', blank = True, default = 'profile-photos/user_ico.png')
    following = models.ManyToManyField(User, related_name='follows')
    updated_at = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return self.text
    def __str__(self):
        return self.__unicode__()

class Tag(models.Model):
    name = models.CharField(max_length=16)
    def __unicode__(self):
        return self.text
    def __str__(self):
        return self.__unicode__()

class Course(models.Model):
    name = models.CharField(max_length=128)
    semester = models.CharField(max_length=3) # Create choices
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TODO: Possobly move to a permission-based model instead of rule-based (last sprint)
    students = models.ManyToManyField(User, related_name='courses_taken')
    staff = models.ManyToManyField(User, related_name='courses_assisted')
    instructors = models.ManyToManyField(User, related_name='courses_managed')
    tags = models.ManyToManyField(Tag, related_name='tag_courses')

    def __unicode__(self):
        return self.name
    def __str__(self):
        return self.__unicode__()


class Post(models.Model):
    header = models.CharField(max_length=128)
    text = models.TextField()
    author = models.ForeignKey(Person,related_name='posts')
    parent_id = models.ForeignKey('Post',related_name='children',default=None)

    ANONYMITY_CHOICES = (('0', 'public'),('1', 'anonymous_to_students'),('2', 'anonymous_to_all'))
    visibility =  models.CharField(max_length=1, choices=ANONYMITY_CHOICES,  default='0')

    POST_TYPES = (('0', 'post'),('1', 'student_reply'),('2', 'staff_reply'),('3', 'comments'))
    timestamp = models.DateTimeField(auto_now=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.header
    def __str__(self):
        return self.__unicode__()


class Assignment(models.Model):
    title = models.CharField(max_length=128)
    course = models.OneToOneField(Course,related_name='assignments')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
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
    title = models.CharField(max_length=128)
    resource_type = models.CharField(max_length=16) # TODO: ENUMERATE
    comments = models.ForeignKey(Post,related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='tag_resources')

    def __unicode__(self):
        return self.title
    def __str__(self):
        return self.__unicode__()


class Team(models.Model):
    team_name = models.CharField(max_length=128)
    assignment = models.ForeignKey(Assignment, related_name='teams') 
    members = models.ManyToManyField(Person, related_name='teams')

    def __unicode__(self):
        return self.team_name
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
     
# TODO: Create Event model for logs

