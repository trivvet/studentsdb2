# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

class MainUser(User):
    """Exam Model"""

    language = models.CharField(
        verbose_name=_(u"Language"),
        max_length=10,
        blank=False
    )

    time_zone = models.CharField(
        verbose_name=_(u"Time Zone"),
        max_length=128,
        blank=True
    )
