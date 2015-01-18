from django.conf.urls import patterns, include, url
from django.contrib import admin
from reunionite.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PollPy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^register/$', register.RegisterView.as_view(), name="register"),
    url(r'^user/$', user.UserView.as_view(), name="user"),
    url(r'^user/(?P<uid>\d+)$', user.UserView.as_view(), name="user"),
    url(r'^$', home.HomeView.as_view(), name="home"),
    url(r'^meetings/$', meetings.PollsView.as_view(), name="meetings"),
    url(r'^meetings/(?P<polls_offset>\d+)/$', meetings.PollsView.as_view(), name="meetings"),
    url(r'^meeting/create$', create_meeting.CreateMeetingView.as_view(), name="create"),
    url(r'^meeting/(?P<poll_id>\d+)$', meeting.PollView.as_view(), name="meeting"),
    url(r'^meeting/(?P<poll_id>\d+)/results$', results.PollResultsView.as_view(), name="results"),
    url(r'^meeting/(?P<poll_id>\d+)/edit$', edit_meeting.EditPollView.as_view(), name="edit"),
    
)
