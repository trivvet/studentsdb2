# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _

class Exam(models.Model):
    """Exam Model"""

    class Meta(object):
        verbose_name=_(u"Exam")
        verbose_name_plural=_(u"Exams")

    name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Subject"))

    date = models.DateTimeField(
        blank=False,
        verbose_name=_(u"Data and time of event"),
        null=True)

    teacher_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Lecturer"))

    exam_group = models.ForeignKey('Group',
        verbose_name=_(u"Group"),
        blank=False,
        null=True,
        on_delete=models.CASCADE)

    notes = models.TextField(
        blank=True,
        verbose_name=_(u"Additional notes"))

    is_completed = models.BooleanField(
        blank=True,
        default=False)

    def __unicode__(self):
        return u"%s (%s, %s), %s - %s" % (self.name, self.exam_group.title,
        self.date.date(), _("completed"), self.is_completed)
