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
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^register$', plaza_views.register, name='register'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', plaza_views.confirm_registration, name='confirm'),

    url(r'^login$', auth_views.login, {'template_name':'login.html'}, name='login'),
    url(r'^logout$', auth_views.logout_then_login, name='logout'),

    url(r'^administration/(?P<id>\d+)$', plaza_views.administration_page, name='administration'),

    url(r'^$', plaza_views.home_page, name='home'),
    url(r'^home/(?P<status>[\w|\W]{,})/(?P<error>[\w|\W]{,})$', plaza_views.home_page_with_msg, name='home_msg'),
    url(r'^staffhome/(?P<id>\d+)$', plaza_views.staffhome_page, name='staffhome'), # Does staffhome need a separate URL endpoint, shouldn't it use the same URL, just check the role

    url(r'^profile/(?P<id>\d+)$', plaza_views.profile_page, name='profile'),
    url(r'^editprofile$', plaza_views.edit_profile_page, name='editprofile'),
    url(r'^profilepicture/(?P<id>\d+)$', plaza_views.get_profile_picture, name='profilepicture'),

    url(r'^createcourse$', plaza_views.course_creation_page, name='createcourse'),
    url(r'^editcourse/(?P<course_semester>\w+)/(?P<course_number>\d+)$',
        plaza_views.edit_course, name='editcourse'),
    url(r'^coursesignup/(?P<course_semester>\w+)/(?P<course_number>\d+)$',
        plaza_views.course_signup_page, name='coursesignup'),

    ## Team urls ##
    url(r'^createteam/(?P<course_semester>\w+)/(?P<course_number>\d+)/(?P<assignment_number>\d+)$',
        plaza_views.team_creation_page, name='createteam'),
    url(r'^staffteamview/(?P<id>\d+)$', plaza_views.staff_team_page, name='staffteamview'),
    url(r'^myteam/(?P<course_semester>\w+)/(?P<course_number>\d+)/(?P<assignment_number>\d+)$',
        plaza_views.my_team_page, name='myteamview'),

    ## Resource urls ##
    # url(r'^resourceslide$', plaza_views.resource_slide_page, name='resourceslide'),
    url(r'^resource/(?P<semester_id>[a-zA-Z][0-9]{2})/(?P<course_id>\d+)/(?P<id>\d+)$', plaza_views.resource_page, name='resource'),
    url(r'^createresource/(?P<semester_id>[a-zA-Z][0-9]{2})/(?P<course_id>\d+)/(?P<id>\d+)$', plaza_views.create_resource, name='createresource'),
    url(r'^deleteresource/(?P<semester_id>[a-zA-Z][0-9]{2})/(?P<course_id>\d+)/(?P<id>\d+)$', plaza_views.delete_resource, name='deleteresource'),
    url(r'^resourceparent/(?P<semester_id>[a-zA-Z][0-9]{2})/(?P<course_id>\d+)/(?P<id>\d+)$', plaza_views.resource_parent, name='resourceparent'),

    url(r'^forum/(?P<semester_id>[a-zA-Z][0-9]{2})/(?P<course_id>\d+)$', plaza_views.forum, name='forum'),
    url(r'^forum_home/(?P<semester_id>[a-zA-Z][0-9]{2})/(?P<course_id>\d+)$', plaza_views.forum_home, name='forum_home'),
    url(r'^view_post/(?P<post_id>-?\d+)$', plaza_views.view_post, name='view_post'),
    url(r'^post/(?P<semester_id>[a-zA-Z][0-9]{2})/(?P<course_id>\d+)/(?P<parent_id>\d+)$', plaza_views.post, name='post'),
    url(r'^edit_post/(?P<post_id>\d+)$', plaza_views.edit_post, name='edit_post'),
    url(r'^delete_post/(?P<id>\d+)$', plaza_views.delete_post, name='delete_post'),

    url(r'^upvote/(?P<post_id>\d+)$', plaza_views.upvote, name='upvote'),
    url(r'^downvote/(?P<post_id>\d+)$', plaza_views.downvote, name='downvote'),

    url(r'^followtag/(?P<id>\d+)$', plaza_views.follow_tag, name='followtag'),
    url(r'^unfollowtag/(?P<id>\d+)$', plaza_views.unfollow_tag, name='unfollowtag'),

    url(r'^followuser/(?P<id>\d+)$', plaza_views.follow_user, name='followuser'),
    url(r'^unfollowuser/(?P<id>\d+)$', plaza_views.unfollow_user, name='unfollowuser'),

    ## Notification URL ##
    url(r'^notification$', plaza_views.notification_page, name='notification'),
    url(r'^getnotification/(?P<id>\d+)$', plaza_views.get_notification, name='getnotification'),
    url(r'^markreadnoti/(?P<id>\d+)$', plaza_views.mark_as_read, name='markreadnoti'),
    url(r'^unreadnumber$', plaza_views.unread_number, name='unreadnumber'),

    # AJAX urls
    url(r'^search_student/$', plaza_views.search_student, name='searchstudent'),
    url(r'^submit_team/$', plaza_views.submit_team, name='submitteam'),
    url(r'^add_person_to_team/$', plaza_views.add_person_to_team, name='addpersontoteam'),
    url(r'^remove_person_from_team/$', plaza_views.remove_person_from_team,
            name='removepersonfromteam'),

    url(r'^save_course_pref/(?P<course_semester>\w+)/(?P<course_number>\d+)/$',
        plaza_views.save_course_pref, name='savecoursepref'),
    url(r'^add_person_to_course/$', plaza_views.add_person_to_course, name='addpersontocourse'),
    url(r'^add_tag_to_course/$', plaza_views.add_tag_to_course,
            name='addtagtocourse'),
    url(r'^remove_tag_from_course/$', plaza_views.remove_tag_from_course,
            name='removetagfromcourse'),

    url(r'^add_assignment_to_course/$', plaza_views.add_assignment_to_course,
            name='addassignmenttocourse'),
    url(r'^remove_assignment_from_course/$', plaza_views.remove_assignment_from_course,
            name='removeassignmentfromcourse'),
    url(r'^remove_person_from_course/$', plaza_views.remove_person_from_course,
            name='removepersonfromcourse'),
    url(r'^dynamic_obj_suggestion/', plaza_views.dynamic_obj_suggestion,
            name='dynamicobjsuggestion'),
    url(r'^get_new_posts_json/(?P<semester_id>[a-zA-Z][0-9]{2})/(?P<course_id>\d+)/(?P<post_id>\d+)$',plaza_views.get_new_posts_json, name='get_new_posts_json'),

    # Rich Text uses TinyMCE
    url(r'^tinymce/', include('tinymce.urls')),

    # account setting
    url(r'^account/$', plaza_views.account_page, name='account'),
    url(r'^changepassword$', plaza_views.change_password, name='changepassword'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
