# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from datetime import date

class Journal(models.Model):
    """Journal Model"""

    class Meta(object):
        verbose_name=u"Відвідування"
        verbose_name_plural=u"Відвідування"

    student_name = models.ForeignKey('Student',
        verbose_name=u"Студент",
        blank=False,
        null=True,
        on_delete=models.PROTECT)

    month = models.DateField(
        verbose_name=u"Місяць",
        blank=False,
        default=date.today())
        
    for day in range(1, date)    
    

    def __unicode__(self):
        return u"%s %s" % (self.student_id.first_name, 
            self.students_id.last_name)
