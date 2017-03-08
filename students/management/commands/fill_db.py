from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from students.models import Student, Group, Exam

class Command(BaseCommand):
    help = 'Fills database of custom elements'

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument('--students')
        parser.add_argument('--groups')
        parser.add_argument('--exams')
        parser.add_argument('--users')

    def handle(self, *args, **options):
        if options['groups'] is not None:
            for i in range(1,int(options['groups'])+1):
                group = Group.objects.get_or_create(title="Start%s" % i)
                group.save()
        
        if options['students'] is not None:
            if Group.objects.count() == 0:
                group = Group.objects.get_or_create(title="Start1")
                group.save()
                    
            for i in range(1,int(options['students'])+1):
                group_for_student = Group.objects.all()[min(i, Group.objects.count())]
                student = Student.objects.get_or_create(first_name="Student%s" % i, last_name="Member%s" % i, birthday=datetime.today().date() - relativedelta(years=17+i), ticket="12%s" % (i + 1), student_group=group_for_student)
                student.save()

        if options['exams'] is not None:
            if Group.objects.count() == 0:
                group = Group(title="Start1")
                group.save()

            for i in range(1,int(options['exams'])+1):
                group_for_exam = Group.objects.all()[min(i, Group.objects.count())]
                exam = Exam.objects.get_or_create(name="Exam%s" % i, date=datetime.today(), teacher_name="Teacher%s" % i, exam_group=group_for_exam)
                exam.save()

        if options['users'] is not None:
            for i in range(1,int(options['users'])+1):
                user = User.objects.create_user(username='User%s' % i,
                                 email='%s@test.com' % i,
                                 password='12345678',
                                 is_active=True)
                
