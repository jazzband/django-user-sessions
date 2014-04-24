from django.test import TestCase
from django.test.client import Client

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.utils.importlib import import_module
from django.http import HttpRequest, SimpleCookie

class Client(Client):

    def login(self, **credentials):
        """
        Sets the Factory to appear as if it has successfully logged into a site.

        Returns True if login is possible; False if the provided credentials
        are incorrect, or the user is inactive, or if the sessions framework is
        not available.
        """
        user = authenticate(**credentials)
        if user and user.is_active \
                and 'user_sessions' in settings.INSTALLED_APPS:
            engine = import_module(settings.SESSION_ENGINE)

            # Create a fake request to store login details.
            request = HttpRequest()
            if self.session:
                request.session = self.session
            else:
                request.session = engine.SessionStore('ua', '127.0.0.1')
            login(request, user)

            # Save the session values.
            request.session.save()

            # Set the cookie to represent the session.
            session_cookie = settings.SESSION_COOKIE_NAME
            self.cookies[session_cookie] = request.session.session_key
            cookie_data = {
                'max-age': None,
                'path': '/',
                'domain': settings.SESSION_COOKIE_DOMAIN,
                'secure': settings.SESSION_COOKIE_SECURE or None,
                'expires': None,
            }
            self.cookies[session_cookie].update(cookie_data)

            return True
        else:
            return False

    def logout(self):
        """
        Removes the authenticated user's cookies and session object.

        Causes the authenticated user to be logged out.
        """
        session = import_module(settings.SESSION_ENGINE).SessionStore('ua', '127.0.0.1')
        session_cookie = self.cookies.get(settings.SESSION_COOKIE_NAME)
        if session_cookie:
            session.delete(session_key=session_cookie.value)
        self.cookies = SimpleCookie()

class TestCase(TestCase):
    """Our Client should use the user_session"""
    client_class = Client

