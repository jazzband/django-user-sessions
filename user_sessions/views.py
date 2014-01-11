from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
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
        return super(LoginRequiredMixin, self).dispatch(request, *args,
                                                        **kwargs)


class SessionListView(LoginRequiredMixin, SessionMixin, ListView):
    """
    View for listing a user's own sessions.

    This view shows list of a user's currently active sessions. You can
    override the template by providing your own template at
    `user_sessions/session_list.html`.
    """
    def get_context_data(self, **kwargs):
        kwargs['session_key'] = self.request.session.session_key
        return super(SessionListView, self).get_context_data(**kwargs)


class SessionDeleteView(LoginRequiredMixin, SessionMixin, DeleteView):
    """
    View for deleting a user's own session.

    This view allows a user to delete an active session. For example locking
    out a session from a computer at the local library or a friend's place.
    """
    def get_success_url(self):
        return str(reverse_lazy('user_sessions:session_list'))
