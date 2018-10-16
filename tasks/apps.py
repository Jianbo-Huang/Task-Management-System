from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MtasksConfig(AppConfig):
    name = 'tasks'
    verbose_name = _(' Task Management')
