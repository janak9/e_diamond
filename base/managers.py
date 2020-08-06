from django.db import models
from base import const

class StatusManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.active_only = kwargs.pop('active_only', True)
        super(StatusManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.active_only:
            return super().get_queryset().filter(status=const.ACTIVE)
        return super().get_queryset().all()
