# -*- coding: utf-8 -*-

import logging

from django.db.models.signals import post_save, post_delete
from django.core.signals import request_finished, request_started
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver, Signal
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from models import Student, Group, Exam, MonthJournal, Result, LogEntry

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

    logger_info = ''
    signal_name = sender.__doc__ + ' is ' + log

    if sender == Student:
        student = kwargs['instance']
        logger.info(u'Student %s: %s %s (ID: %d)', log, student.first_name, student.last_name, student.id)
        logger_info = u'Student %s: %s %s (ID: %d)' % (log, student.first_name, student.last_name, student.id)
    elif sender == Group:
        group = kwargs['instance']
        logger.info(u'Group %s: %s (ID: %d)', log, group.title, group.id)
        logger_info = u'Group %s: %s (ID: %d)' % (log, group.title, group.id)
    elif sender == Exam:
        exam = kwargs['instance']
        try:
            exam_group = exam.exam_group.title
        except ObjectDoesNotExist:
            exam_group = 'Deleted Group'
        logger.info(u'Exam %s: %s for %s (ID: %d)', log, exam.name, exam_group, exam.id)
        logger_info = u'Exam %s: %s for %s (ID: %d)' % (log, exam.name, exam_group, exam.id)
    elif sender == Result:
        result = kwargs['instance']
        try:
            first_name = result.result_student.first_name
            last_name = result.result_student.last_name
        except ObjectDoesNotExist:
            first_name = 'Already'
            last_name = 'Deleted'
        logger.info(u'Result %s: Student %s %s got mark %s for %s (ID: %d)',
            log, first_name, last_name, result.score, result.result_exam.name, result.id)
        logger_info = u'Result %s: Student %s %s got mark %s for %s (ID: %d)' % (
            log, first_name, last_name, result.score, result.result_exam.name, result.id)
        signal_name = 'Result Model is ' + log
    elif sender == MonthJournal:
        journal = kwargs['instance']
        month_name = [_(u'Січень'), _(u'Лютий'), _(u'Березень'),
            _(u'Квітень'), _(u'Травень'), _(u'Червень'), _(u'Липень'),
            _(u'Серпень'), _(u'Вересень'), _(u'Жовтень'), _(u'Листопад'), _(u'Грудень')]
        logger.info(u'Journal %s: Student %s %s for %s (ID: %d)', log, journal.student_name.first_name, journal.student_name.last_name, month_name[journal.date.month-1], journal.id)
        logger_info = u'Journal %s: Student %s %s for %s (ID: %d)' % (log, journal.student_name.first_name, journal.student_name.last_name, month_name[journal.date.month-1], journal.id)
    elif sender == User:
        user = kwargs['instance']
        logger.info(u'User %s: %s', log, user.username)
        logger_info = u'User %s: %s' % (log, user.username)
        signal_name = 'User Model is ' + log
    else:
        logger_info = False

    if logger_info:
        # import pdb;pdb.set_trace()
        current_time = timezone.now()
        log = LogEntry(log_datetime=current_time, status='INFO', signal=signal_name, info=logger_info)
        log.save()

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
    current_time = timezone.now()
    logger_info = u'Send mail to Admin from %s, Theme - %s' % (email, subject)
    log = LogEntry(log_datetime=current_time, status="INFO", signal='Send mail to Admin', info=logger_info)
    log.save()

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
