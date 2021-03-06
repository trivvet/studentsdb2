from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.utils import translation
from django.conf import settings

from students.models import Student, Group

class Command(BaseCommand):
    help = _(u'Displays number of model objects in database')

    models = (('student', Student), ('group', Group), ('user', User))

    def add_arguments(self, parser):
        parser.add_argument('model_name', nargs='+', type=str)

    def handle(self, *args, **options):
#        import pdb;pdb.set_trace()
        translation.activate(settings.LANGUAGE_CODE)

        for model_name, model in self.models:
            if model_name in options['model_name']:
                self.stdout.write(_(u"Number of {model}s in database: {amount}").format(
                    model=model_name,
                    amount=model.objects.count()
                ))
