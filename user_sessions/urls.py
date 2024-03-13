from django.urls import path

from .views import SessionDeleteOtherView, SessionDeleteView, SessionListView

app_name = 'user_sessions'
urlpatterns = [
    path(
        'sessions/',
        view=SessionListView.as_view(),
        name='session_list',
    ),
    path(
        'sessions/other/delete/',
        view=SessionDeleteOtherView.as_view(),
        name='session_delete_other',
    ),
    path(
        'account/sessions/<str:pk>/delete/',
        view=SessionDeleteView.as_view(),
        name='session_delete',
    ),
]
