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
    