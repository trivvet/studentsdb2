# -*- coding: utf-8 -*-

import logging, sys
from datetime import datetime, date
from StringIO import StringIO

from django.test import TestCase, override_settings
from django.contrib.auth.models import User

from students.models import Student, Group, Exam, Result, MonthJournal

reload(sys)  
sys.setdefaultencoding('utf8')

@override_settings(LANGUAGE_CODE='en')

class SignalsTest(TestCase):

    def setUp(self):
        # add our root handler
        self.out = StringIO()
        self.handler = logging.StreamHandler(self.out)
        logging.root.addHandler(self.handler)
        self.time_now = datetime.now()
        self.group = Group(title='DemoGroup')
        self.student = Student(first_name='Demo', last_name="Student",
            ticket='1', birthday='1980-01-01', student_group=self.group)
        self.exam = Exam(name="Math", date=self.time_now,
            teacher_name="Visiliy Ivanov", exam_group=self.group)
        self.result = Result(result_student=self.student,
            result_exam=self.exam, score=10)
        
    def tearDown(self):
        # remove root handler
        logging.root.removeHandler(self.handler)
        
    def test_update_student(self):

        # create new group and student
        self.group.save()
        self.student.save()

        # test signal of created students
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1],
            'Student added: Demo Student (ID: %s)\n' % self.student.id)

        self.student.ticket = 5
        self.student.save()

        # test signal of updated students
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1],
            'Student updated: Demo Student (ID: %s)\n' % self.student.id)

    def test_delete_student(self):

        # create new group and student
        self.group.save()
        self.student.save()

        # test signal of deleted students
        student_id = self.student.id
        self.student.delete()
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1],
            'Student deleted: Demo Student (ID: %s)\n' % student_id)
    
    def test_update_group(self):

        # create new group
        self.group.save()

        # test signal of created students
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1],
            'Group added: DemoGroup (ID: %s)\n' % self.group.id)

        self.group.notes = 'abc'
        self.group.save()

        # test signal of updated groups
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1],
            'Group updated: DemoGroup (ID: %s)\n' % self.group.id)

    def test_delete_group(self):

        # create new group
        self.group.save()

        # test signal of deleted groups
        group_id = self.group.id
        self.group.delete()
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1],
            'Group deleted: DemoGroup (ID: %s)\n' % group_id)
        
    def test_update_exam(self):

        # create new group and exam
        self.group.save()
        self.exam.save()

        # test signal of created exams
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1],
            'Exam added: Math for DemoGroup (ID: %s)\n' % self.exam.id)

        self.exam.teacher_name = 'Vasiliy Ivanov'
        self.exam.save()

        # test signal of updated exams
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1],
            'Exam updated: Math for DemoGroup (ID: %s)\n' % self.exam.id)

    def test_delete_exam(self):

        # create new group and exam
        self.group.save()
        self.exam.save()

        # test signal of deleted exams
        exam_id = self.exam.id
        self.exam.delete()
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1],
            'Exam deleted: Math for DemoGroup (ID: %s)\n' % exam_id)

    def test_update_result(self):

        # create new group, student, exam and result
        self.group.save()
        self.student.save()
        self.exam.save()
        self.result.save()

        # test signal of created results
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1],
            'Result added: Student Demo Student got mark 10 for Math (ID: %s)\n' % self.result.id)

        self.result.score = 11
        self.result.save()

        # test signal of updated results
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1],
            'Result updated: Student Demo Student got mark 11 for Math (ID: %s)\n' % self.result.id)

    def test_delete_result(self):

        # create new group, student, exam and result
        self.group.save()
        self.student.save()
        self.exam.save()
        self.result.save()

        # test signal of deleted results
        result_id = self.result.id
        self.result.delete()
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1],
            'Result deleted: Student Demo Student got mark 10 for Math (ID: %s)\n' % result_id)

    def test_update_journal(self):

        # create new group, student and journal
        self.group.save()
        self.student.save()
        student_journal = MonthJournal(student_name=self.student,
            date=date(datetime.today().year, datetime.today().month, 1))
        student_journal.save()

        month_name = [u'Січень', u'Лютий', u'Березень', u'Квітень',
            u'Травень', u'Червень', u'Липень', u'Серпень', u'Вересень',
            u'Жовтень', u'Листопад', u'Грудень']

        # test signal of created journals
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1],
            'Journal added: Student Demo Student for %s (ID: %s)\n' %
            (month_name[student_journal.date.month-1], student_journal.id))

        student_journal.score = 11
        student_journal.save()

        # test signal of updated journals
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1],
            'Journal updated: Student Demo Student for %s (ID: %s)\n' %
            (month_name[student_journal.date.month-1], student_journal.id))

    def test_delete_journal(self):

        # create new group, student and journal
        self.group.save()
        self.student.save()
        student_journal = MonthJournal(student_name=self.student,
            date=date(datetime.today().year, datetime.today().month, 1))
        student_journal.save()
        month_name = [u'Січень', u'Лютий', u'Березень', u'Квітень',
            u'Травень', u'Червень', u'Липень', u'Серпень', u'Вересень',
            u'Жовтень', u'Листопад', u'Грудень']

        # test signal of deleted journals
        student_journal_id = student_journal.id
        student_journal.delete()
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1],
            'Journal deleted: Student Demo Student for %s (ID: %s)\n' %
            (month_name[student_journal.date.month-1], student_journal_id))

    def test_user_update(self):
        # create new user
        user = User.objects.create_user(username='trivvet2')
        
        # test signal of created users
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1],
            'User added: trivvet2\n')

        # test signal of updated users
        user.password = 'trivvet2345'
        user.save()
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1],
            'User updated: trivvet2\n')

    def test_user_deleted(self):
        # create new user
        user = User.objects.create_user(username='trivvet2')

        # test signal of deleted users
        user.delete()
        self.out.seek(0)
        self.assertEqual(self.out.readlines()[-1],
            'User deleted: trivvet2\n')
        
        
