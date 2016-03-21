"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include,url
from plaza import views as plaza_views

urlpatterns = [
    url(r'^$', plaza_views.base, name='base'),
   """
    url(r'^$', plaza_views.home_page, name='home'),
    url(r'^profile/(?P<id>\d+)$', plaza_views.profile_page, name='profile'),
    url(r'^editprofile$', plaza_views.edit_profile_page, name='editprofile'),
    url(r'^administration/(?P<id>\d+)$', plaza_views.administration_page, name='administration'),
    url(r'^createcourse$', plaza_views.course_creation_page, name='createcourse'),
    url(r'^editcourse/(?P<id>\d+)$', plaza_views.edit_post, name='editcourse'), # Maybe also delete a course?
    url(r'^createteam$', plaza_views.create_team, name='createteam'),
    url(r'^resourceslide$', plaza_views.resource_slide_page, name='resourceslide'),
    url(r'^makepost$', plaza_views.make_post, name='makepost'),
    url(r'^editpost/(?P<id>\d+)$', plaza_views.edit_post, name='editpost'),
    url(r'^deletepost/(?P<id>\d+)$', plaza_views.delete_post, name='deletepost'),
    url(r'^makecomment$', plaza_views.make_comment, name='makecomment'),
    url(r'^deletecomment/(?P<id>\d+)$', plaza_views.delete_comment, name='deletecomment'),
    url(r'^followtag/(?P<id>\d+)$', plaza_views.follow_tag, name='followtag'),
    url(r'^unfollowtag/(?P<id>\d+)$', plaza_views.unfollow_tag, name='unfollowtag'),
    url(r'^upvote/(?P<id>\d+)$', plaza_views.upvote, name='upvote'),
    url(r'^downvote/(?P<id>\d+)$', plaza_views.downvote, name='downvote'),
    url(r'^getpost$', plaza_views.get_post, name='getpost'),
    url(r'^getnotification$', plaza_views.get_nofitcation, name='getnotification'),
    url(r'^resource$', plaza_views.resource_page, name='resource'),
    url(r'^uploadr$', plaza_views.uoload_resource, name='uploadr'),
    url(r'^register$', plaza_views.register, name='register'),
    url(r'^login$', auth_views.login, {'template_name':'login.html'}, name='login'),
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$',
        plaza_views.confirm_registration, name='confirm'),
   """
]
