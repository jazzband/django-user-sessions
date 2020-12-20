from django.urls import include, path
from django.contrib import admin
from django.http import HttpResponse

admin.autodiscover()


def empty(request):
    return HttpResponse('')


def modify_session(request):
    request.session['FOO'] = 'BAR'
    return HttpResponse('')


urlpatterns = [
    path('', empty),
    path('modify_session/', modify_session),
    path('admin/', admin.site.urls),
    path('', include('user_sessions.urls', namespace='user_sessions')),
]
