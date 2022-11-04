from django.conf import settings
from django.contrib import admin
from django.urls import include, re_path, reverse_lazy
from django.views.generic.base import RedirectView

admin.autodiscover()

urlpatterns = [
    re_path(
        '^$',
        RedirectView.as_view(
            url=reverse_lazy('user_sessions:session_list'),
            permanent=True,
        ),
        name='home',
    ),
    re_path(r'', include('user_sessions.urls', namespace='user_sessions')),
    re_path(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
