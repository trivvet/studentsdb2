# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

class Exam(models.Model):
    """Exam Model"""

    class Meta(object):
        verbose_name=u"Іспит"
        verbose_name_plural=u"Іспити"

    name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Предмет")

    date = models.DateTimeField(
        blank=False,
        verbose_name=u"Дата та час проведення",
        null=True)

    teacher_name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Викладач")

    exam_group = models.ForeignKey('Group',
        verbose_name=u"Група",
        blank=False,
        null=True,
        on_delete=models.PROTECT)

    def __unicode__(self):
        return u"%s (%s %s)" % (self.name, self.teacher_name,
            self.exam_group.title)
