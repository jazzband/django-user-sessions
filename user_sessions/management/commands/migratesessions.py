# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand
from user_sessions.models import Session as UserSession
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
    def add_arguments(self, parser):
        parser.add_argument('--oldmodel',
                            dest='oldmodel',
                            default='django.contrib.sessions.models.Session',
                            help='Existing session model to migrate to the new UserSessions database table')

    def handle(self, *args, **options):
        User = get_user_model()
        old_sessions = get_model_class(options['oldmodel']).objects.all()
        logger.info("Processing %d session objects" % old_sessions.count())
        conversion_count = 0
        for old_session in old_sessions:
            if not UserSession.objects.filter(session_key=old_session.session_key).exists():
                data = old_session.get_decoded()
                user = User.objects.filter(pk=data['_auth_user_id']).first() if '_auth_user_id' in data else None
                UserSession.objects.create(
                    session_key=old_session.session_key,
                    session_data=old_session.session_data,
                    expire_date=old_session.expire_date,
                    user=user,
                    ip='127.0.0.1'
                )
                conversion_count += 1

        logger.info("Created %d new session objects" % conversion_count)
