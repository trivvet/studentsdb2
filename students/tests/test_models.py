from datetime import date, datetime

from django.test import TestCase, override_settings

from students.models import Student, Group, MonthJournal, Exam, Result, LogEntry

@override_settings(LANGUAGE_CODE='en')

class ModelsTest(TestCase):

    def setUp(self):
        self.student = Student(first_name="Demo", last_name="Student")
        self.group = Group(title="Demo Group")
        self.time_now = datetime.now()
        self.exam = Exam(name="Math", date=self.time_now, teacher_name="Visiliy Ivanov", exam_group=self.group)

    def test_student_unicode(self):
        # check unicode string of Student model
        self.assertEqual(unicode(self.student), u"Demo Student")

    def test_group_unicode(self):
        # check unicode string of Group model
        self.assertEqual(unicode(self.group), "Demo Group")

        self.group.leader = self.student
        self.assertEqual(unicode(self.group), "Demo Group (Demo Student)")
        
    def test_journal_unicode(self):
        # check unicode string of Journal model
        student_journal = MonthJournal(student_name=self.student, date=date(datetime.today().year, datetime.today().month, 1))
        self.assertEqual(unicode(student_journal), "Student: %d %d" % (date.today().month, date.today().year))

    def test_exam_unicode(self):
        # check unicode string of Exam model
        self.assertEqual(unicode(self.exam), "Math (Demo Group, %s), completed - False" % self.time_now.date())
        
    def test_result_unicode(self):
        result = Result(result_student=self.student, result_exam=self.exam, score=10)
        self.assertEqual(unicode(result), "Student Demo (Math %s)" % self.time_now.date())

    def test_log_unicode(self):
        self.group.save()
        log = LogEntry.objects.all()[0]
        self.assertEqual(unicode(log), "INFO Group Model is added (%s)" % datetime.strftime(log.log_datetime, '%Y-%m-%d %H:%M:%S'))
