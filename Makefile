TARGET?=tests

.PHONY: ruff example test coverage

ruff:
	ruff user_sessions example tests

example:
	DJANGO_SETTINGS_MODULE=example.settings PYTHONPATH=. \
		django-admin.py runserver

check:
	DJANGO_SETTINGS_MODULE=example.settings PYTHONPATH=. \
		python -Wd example/manage.py check

generate-mmdb-fixtures:
	docker --context=default buildx build -f tests/Dockerfile --tag test-mmdb-maker tests
	docker run --rm --volume $$(pwd)/tests:/data test-mmdb-maker

test: generate-mmdb-fixtures
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
