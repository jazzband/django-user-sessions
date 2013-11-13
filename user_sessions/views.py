from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.generic import ListView, DeleteView


class SessionMixin(object):
    def get_queryset(self):
        return self.request.user.session_set\
            .filter(expire_date__gt=now()).order_by('-last_activity')


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class SessionListView(LoginRequiredMixin, SessionMixin, ListView):
    def get_context_data(self, **kwargs):
        kwargs['session_key'] = self.request.session.session_key
        return super(SessionListView, self).get_context_data(**kwargs)


class SessionDeleteView(LoginRequiredMixin, SessionMixin, DeleteView):
    pass
