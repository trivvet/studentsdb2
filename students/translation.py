from django.utils.translation import ugettext as _

from modeltranslation.translator import register, TranslationOptions

from models import Student

@register(Student)
class NewsTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name')
    required_languages = ('uk', 'en', 'ru')

