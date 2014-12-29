# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand
from optparse import make_option
from user_sessions.models import Session as NewSession
from django.contrib.auth import get_user_model
import logging
import importlib

logger = logging.getLogger(__name__)


def get_model_class(full_model_name):
    old_model_package, old_model_class_name = full_model_name.rsplit('.', 1)
    package = importlib.import_module(old_model_package)
    return getattr(package, old_model_class_name)


class Command(BaseCommand):
    """
    Convert existing (old) sessions to the new session store.
    """
    option_list = BaseCommand.option_list + (
        make_option('--oldmodel',
                    dest='oldmodel',
                    default='django.contrib.sessions.models.Session',
                    help='Existing session model to migrate to the new Session database'),
    )

    def handle(self, *args, **options):
        user_model = get_user_model()
        old_sessions = get_model_class(options['oldmodel']).objects.all()
        logger.info("Processing %d session objects" % old_sessions.count())
        conversion_count = 0
        for old_session in old_sessions:
            if not NewSession.objects.filter(session_key=old_session.session_key).exists():
                data = old_session.get_decoded()
                user = None
                if '_auth_user_id' in data:
                    users = user_model.objects.filter(pk=data['_auth_user_id'])
                    user = users[0] if users else None
                new_session = NewSession(session_key=old_session.session_key,
                                         session_data=old_session.session_data,
                                         expire_date=old_session.expire_date,
                                         user=user,
                                         ip='127.0.0.1')
                new_session.save()
                conversion_count += 1

        logger.info("Created %d new session objects" % conversion_count)
