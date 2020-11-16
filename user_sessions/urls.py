from django.conf.urls import url
from user_sessions.views import SessionDeleteOtherView

from .views import SessionDeleteView, SessionListView

app_name = 'user_sessions'
urlpatterns = [
    url(
        regex=r'^$',
        view=SessionListView.as_view(),
        name='session_list',
    ),
    url(
        regex=r'^other/delete/$',
        view=SessionDeleteOtherView.as_view(),
        name='session_delete_other',
    ),
    url(
        regex=r'^(?P<pk>\w+)/delete/$',
        view=SessionDeleteView.as_view(),
        name='session_delete',
    ),
]
