from django.conf.urls import include, url

from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

admin.autodiscover()

urlpatterns = [
    url(
        regex=r'^$',
        view=RedirectView.as_view(
            url=reverse_lazy('user_sessions:session_list'),
            permanent=True,
        ),
        name='home',
    ),
    url(r'', include('user_sessions.urls')),
    url(r'^admin/', admin.site.urls),
]
