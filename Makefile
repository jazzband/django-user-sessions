.PHONY: flake8 example test compress_js compress_css translatable_strings update_translations

flake8:
	flake8 debug_toolbar example tests

test:
	DJANGO_SETTINGS_MODULE=tests.settings PYTHONPATH=. \
		django-admin.py test tests

coverage:
	coverage erase
	DJANGO_SETTINGS_MODULE=tests.settings PYTHONPATH=. \
		coverage run --branch --source=user_sessions `which django-admin.py` \
		test tests
	coverage html
