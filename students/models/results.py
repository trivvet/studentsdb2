# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

class Result(models.Model):
    """Exam Model"""

    class Meta(object):
        verbose_name=u"Результат іспиту"
        verbose_name_plural=u"Результати іспитів"

    result_student = models.ForeignKey('Student',
        verbose_name=u"Студент",
        blank=False,
        null=True,
        on_delete=models.CASCADE)

    result_exam = models.ForeignKey('Exam',
        verbose_name=u"Предмет",
        blank=False,
        null=True,
        on_delete=models.PROTECT)
   
    score = models.IntegerField(
        verbose_name = u"Оцінка",
        blank = False)

    def __unicode__(self):
        return u"%s %s (%s %s)" % (self.result_student.last_name, 
            self.result_student.first_name, self.result_exam.name,
            self.result_exam.date.date())
