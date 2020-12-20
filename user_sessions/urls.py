from django.urls import path, re_path

from user_sessions.views import SessionDeleteOtherView

from .views import SessionDeleteView, SessionListView

app_name = 'user_sessions'
urlpatterns = [
    path('account/sessions/',
        view=SessionListView.as_view(),
        name='session_list',
    ),
    path('account/sessions/other/delete/',
        view=SessionDeleteOtherView.as_view(),
        name='session_delete_other',
    ),
    re_path(
        r'^account/sessions/(?P<pk>\w+)/delete/$',
        view=SessionDeleteView.as_view(),
        name='session_delete',
    ),
]
