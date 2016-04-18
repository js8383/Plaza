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
from django.contrib.auth import views as auth_views
from plaza import views as plaza_views

urlpatterns = [
    url(r'^register$', plaza_views.register, name='register'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', plaza_views.confirm_registration, name='confirm'),

    url(r'^login$', auth_views.login, {'template_name':'login.html'}, name='login'),
    url(r'^logout$', auth_views.logout_then_login, name='logout'),

    url(r'^administration/(?P<id>\d+)$', plaza_views.administration_page, name='administration'),

    url(r'^$', plaza_views.home_page, name='home'),
    url(r'^staffhome/(?P<id>\d+)$', plaza_views.staffhome_page, name='staffhome'), # Does staffhome need a separate URL endpoint, shouldn't it use the same URL, just check the role

    url(r'^profile/(?P<id>\d+)$', plaza_views.profile_page, name='profile'),
    url(r'^editprofile$', plaza_views.edit_profile_page, name='editprofile'),

    url(r'^viewcourse/(?P<number>\d+)$', plaza_views.view_course_page, name='viewcourse'),
    url(r'^createcourse$', plaza_views.course_creation_page, name='createcourse'),
    url(r'^editcourse/(?P<course_number>\d+)/(?P<course_semester>\w)$', plaza_views.edit_course, name='editcourse'),
    url(r'^managecourses$', plaza_views.manage_courses, name='managecourses'),

    ## Team urls ##
    url(r'^createteam/(?P<course_number>\d+)/(?P<assignment_number>\d+)$',
        plaza_views.team_creation_page, name='createteam'),
    url(r'^staffteamview/(?P<id>\d+)$', plaza_views.staff_team_page, name='staffteamview'),
    url(r'^myteam/(?P<course_number>\d+)/(?P<assignment_number>\d+)$', plaza_views.my_team_page, name='myteamview'),

    ## Resource urls ##
    url(r'^resourceslide$', plaza_views.resource_slide_page, name='resourceslide'),
    url(r'^resource$', plaza_views.resource_page, name='resource'),
    url(r'^uploadr$', plaza_views.upload_resource, name='uploadr'),

    url(r'^forum/(?P<semester_id>[a-zA-Z][0-9]{2})/(?P<course_id>\d+)$', plaza_views.forum, name='forum'),
    url(r'^view_post/(?P<post_id>\d+)$', plaza_views.view_post, name='view_posts'),
    url(r'^post/(?P<semester_id>[a-zA-Z][0-9]{2})/(?P<course_id>\d+)/(?P<parent_id>\d+)$', plaza_views.post, name='post'),
    url(r'^delete_post/(?P<id>\d+)$', plaza_views.delete_post, name='delete_post'),

    url(r'^upvote/(?P<id>\d+)$', plaza_views.upvote, name='upvote'),
    url(r'^downvote/(?P<id>\d+)$', plaza_views.downvote, name='downvote'),

    url(r'^followtag/(?P<id>\d+)$', plaza_views.follow_tag, name='followtag'),
    url(r'^unfollowtag/(?P<id>\d+)$', plaza_views.unfollow_tag, name='unfollowtag'),

    url(r'^getnotification$', plaza_views.get_notification, name='getnotification'),

    # AJAX urls
    url(r'^search_student/$', plaza_views.search_student, name='searchstudent'),
    url(r'^submit_team/$', plaza_views.submit_team, name='submitteam'),
    url(r'^save_course_pref/(?P<course_number>\d+)/(?P<course_semester>\w+)/$',
        plaza_views.save_course_pref, name='savecoursepref'),
    url(r'^add_person_to_course/$', plaza_views.add_person_to_course, name='addpersontocourse'),
    url(r'^add_assignment_to_course/$', plaza_views.add_assignment_to_course,
            name='addassignmenttocourse'),
    url(r'^remove_assignment_from_course/$', plaza_views.remove_assignment_from_course,
            name='removeassignmentfromcourse'),
    url(r'^remove_person_from_course/$', plaza_views.remove_person_from_course,
            name='removepersonfromcourse'),

    url(r'^tinymce/', include('tinymce.urls')),
]

