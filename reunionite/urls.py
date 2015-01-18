from django.conf.urls import patterns, include, url
from django.contrib import admin
from reunionite.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'PollPy.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/resgistration/logout.html'}),
    url(r'^register/$', register.RegisterView.as_view(), name="register"),
    url(r'^user/$', user.UserView.as_view(), name="user"),
    url(r'^user/(?P<uid>\d+)$', user.UserView.as_view(), name="user"),
    url(r'^$', home.HomeView.as_view(), name="home"),
    url(r'^meetings/$', meetings.MeetingsView.as_view(), name="meetings"),
    url(r'^meetings/(?P<meetings_offset>\d+)/$', meetings.MeetingsView.as_view(), name="meetings"),
    url(r'^meeting/create$', create_meeting.CreateMeetingView.as_view(), name="create"),
    url(r'^meeting/(?P<meeting_id>\d+)$', meeting.MeetingView.as_view(), name="meeting"),
    url(r'^meeting/(?P<meeting_id>\d+)/results$', results.MeetingResultsView.as_view(), name="results"),
    url(r'^meeting/(?P<meeting_id>\d+)/edit$', edit_meeting.EditMeetingView.as_view(), name="edit"),
    url(r'^meeting/(?P<meeting_id>\d+)/date/(?P<date_id>\d+)$', date.DateView.as_view(), name="date"),
    url(r'^meeting/(?P<meeting_id>\d+)/date/add$', add_date.AddDateView.as_view(), name="add"),
    
)
