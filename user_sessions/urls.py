from django.conf.urls import patterns, url

from user_sessions.views import SessionListView, SessionDeleteView


urlpatterns = patterns(
    '',

    url(
        regex=r'^account/sessions/$',
        view=SessionListView.as_view(),
        name='session_list',
    ),
    url(
        regex=r'^sessions/(?P<pk>\w+)/delete/$',
        view=SessionDeleteView.as_view(),
        name='session_delete',
    ),
)
