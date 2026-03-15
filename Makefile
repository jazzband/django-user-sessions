TARGET?=tests

.PHONY: ruff example test coverage

ruff:
	ruff user_sessions example tests

example:
	DJANGO_SETTINGS_MODULE=example.settings PYTHONPATH=. \
		django-admin runserver

check:
	DJANGO_SETTINGS_MODULE=example.settings PYTHONPATH=. \
		python -Wd example/manage.py check

generate-mmdb-fixtures:
	[ -e tests/test_city.mmdb ] || python3 generate_mmdb.py

test: generate-mmdb-fixtures
	DJANGO_SETTINGS_MODULE=tests.settings PYTHONPATH=. \
		django-admin test ${TARGET}

migrations:
	DJANGO_SETTINGS_MODULE=tests.settings PYTHONPATH=. \
		django-admin makemigrations user_sessions

coverage:
	coverage erase
	DJANGO_SETTINGS_MODULE=tests.settings PYTHONPATH=. \
		coverage run example/manage.py test ${TARGET}
	coverage html
	coverage report

tx-pull:
	tx pull -a
	cd user_sessions; django-admin compilemessages

tx-push:
	cd user_sessions; django-admin makemessages -l en
	tx push -s
