TARGET?=tests

.PHONY: flake8 example test coverage

flake8:
	flake8 user_sessions example tests

example:
	DJANGO_SETTINGS_MODULE=example.settings PYTHONPATH=. \
		django-admin.py runserver

check:
	DJANGO_SETTINGS_MODULE=example.settings PYTHONPATH=. \
		python -Wd example/manage.py check

test:
	DJANGO_SETTINGS_MODULE=tests.settings PYTHONPATH=. \
		django-admin.py test ${TARGET}

migrations:
	DJANGO_SETTINGS_MODULE=tests.settings PYTHONPATH=. \
		django-admin.py makemigrations user_sessions

coverage:
	coverage erase
	DJANGO_SETTINGS_MODULE=tests.settings PYTHONPATH=. \
		coverage run example/manage.py test ${TARGET}
	coverage html
	coverage report

tx-pull:
	tx pull -a
	cd user_sessions; django-admin.py compilemessages

tx-push:
	cd user_sessions; django-admin.py makemessages -l en
	tx push -s
