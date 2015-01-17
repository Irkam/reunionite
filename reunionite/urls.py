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
    url(r'^polls/$', polls.PollsView.as_view(), name="polls"),
    url(r'^polls/(?P<polls_offset>\d+)/$', polls.PollsView.as_view(), name="polls"),
    url(r'^poll/create$', create_poll.CreatePollView.as_view(), name="create"),
    url(r'^poll/(?P<poll_id>\d+)$', poll.PollView.as_view(), name="poll"),
    url(r'^poll/(?P<poll_id>\d+)/results$', results.PollResultsView.as_view(), name="results"),
    url(r'^poll/(?P<poll_id>\d+)/edit$', edit_poll.EditPollView.as_view(), name="results"),
    
)
