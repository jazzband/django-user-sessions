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
		coverage run --branch --source=user_sessions \
		`which django-admin.py` test tests
	coverage html
	coverage report

tx-pull:
	tx pull -a
	cd user_sessions; django-admin.py compilemessages

tx-push:
	cd user_sessions; django-admin.py makemessages -l en
	tx push -s
