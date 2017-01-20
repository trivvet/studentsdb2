# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Result(models.Model):
    """Exam Model"""

    class Meta(object):
        verbose_name=_(u"Exam results")
        verbose_name_plural=_(u"Exams results")

    result_student = models.ForeignKey('Student',
        verbose_name=_(u"Student"),
        blank=False,
        null=True,
        on_delete=models.CASCADE)

    result_exam = models.ForeignKey('Exam',
        verbose_name=_(u"Subject"),
        blank=False,
        null=True,
        on_delete=models.PROTECT)
   
    score = models.IntegerField(
        verbose_name = _(u"Mark"),
        blank = False)

    def __unicode__(self):
        return u"%s %s (%s %s)" % (self.result_student.last_name, 
            self.result_student.first_name, self.result_exam.name,
            self.result_exam.date.date())
