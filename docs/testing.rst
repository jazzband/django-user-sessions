Testing with Django User Sessions
==================================

Django user sessions needs a special test client if
you use calls like `self.client.login` in your code.

For this reason, your tests should either inherit the TestCase 
provided by django-user-sessions, or your test client should use the test Client from django-user-sessions.

Example for inheriting the TestCase::

	from user_sessions.testclient import TestCase

	class MyTestCase(TestCase):

		def test_mytest(self):
			assert True

Example for using the test client directly::

	from django.test import TestCase
	from user_sessions.testclient import Client

	class MyTestCase(TestCase):

		client_class = Client

		def test_mytest(self):
			assert True
