# -*- coding: utf-8 -*-

import logging

from django.db.models.signals import post_save, post_delete
from django.core.signals import request_finished, request_started
from django.dispatch import receiver, Signal

from models import Student, Group, Exam, MonthJournal, Result

counter = 0
segment = 50

@receiver([post_save, post_delete])
def log_models_changed_signal(sender, **kwargs):

    logger = logging.getLogger(__name__)
    try:
        kwargs['created']
    except:
        kwargs['created'] = None
    if kwargs['created'] is None:
        log = 'deleted'
    elif kwargs['created']:
        log = 'added'
    else:
        log = 'updated'

    if sender == Student:
        student = kwargs['instance']
        logger.info(u'Student %s: %s %s (ID: %d)', log, student.first_name, student.last_name, student.id)
    elif sender == Group:
        group = kwargs['instance']
        logger.info(u'Group %s: %s (ID: %d)', log, group.title, group.id)
    elif sender == Exam:
        exam = kwargs['instance']
        logger.info(u'Exam %s: %s for %s (ID: %d)', log, exam.name, exam.exam_group.title, exam.id)
    elif sender == Result:
        result = kwargs['instance']
        logger.info(u'Result %s: Student %s %s got mark %s for %s (ID: %d)', log, result.result_student.first_name, result.result_student.last_name, result.score, result.result_exam.name, result.id)
    elif sender == MonthJournal:
        journal = kwargs['instance']
        month_name = [u'Січень', u'Лютий', u'Березень', u'Квітень', u'Травень', u'Червень', u'Липень', u'Серпень', u'Вересень', u'Жовтень', u'Листопад', u'Грудень']
        logger.info(u'Journal %s: Student %s %s for %s (ID: %d)', log, journal.student_name.first_name, journal.student_name.last_name, month_name[journal.date.month-1], journal.id)

#@receiver(request_finished)
#def hello_world_callback(sender, **kwargs):
    #print 'Hello World!'

send_mail_done = Signal(providing_args=["subject", "from_email"])

@receiver(send_mail_done)
def log_send_mail_done(sender, **kwargs):
    logger = logging.getLogger(__name__)
    email = kwargs['from_email']
    subject = kwargs['subject']
    logger.info(u'Send mail to Admin from %s, Theme - %s', email, subject)

def log_migrate_dote(sender, **kwargs):
    logger = logging.getLogger(__name__)
    db_info = kwargs['using']
    model_changed = sender.verbose_name
    logger.info(u'Command of manage.py - mirgate is used: %s', db_info)

@receiver(request_started)
def log_request_counter(sender, **kwargs):
    global counter
    global segment
    logger = logging.getLogger(__name__)
    counter += 1
    if counter > segment:
        logger.info(u'Done %s requests', segment)
        segment += 50
