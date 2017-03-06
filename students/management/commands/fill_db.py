from django.core.management.base import BaseCommand

from students.models import Student, Group

class Command(BaseCommand):
    help = 'Fills database of custom elements'

    models = (('student', Student), ('group', Group))

    def add_arguments(self, parser):
        parser.add_argument('model_name', nargs='+', type=str)

    def handle(self, *args, **options):
        for model_name, model in self.models:
            if model_name in options['model_name']:
                self.stdout.write('Number of %ss in database: %d' % (model_name, model.objects.count()))
