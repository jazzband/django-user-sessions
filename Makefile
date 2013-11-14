.PHONY: flake8 example test coverage

flake8:
	flake8 user_sessions example tests

example:
	DJANGO_SETTINGS_MODULE=example.settings PYTHONPATH=. \
		django-admin.py runserver

test:
	DJANGO_SETTINGS_MODULE=tests.settings PYTHONPATH=. \
		django-admin.py test tests

coverage:
	coverage erase
	DJANGO_SETTINGS_MODULE=tests.settings PYTHONPATH=. \
		coverage run --branch --source=user_sessions
		`which django-admin.py` test tests
	coverage html

