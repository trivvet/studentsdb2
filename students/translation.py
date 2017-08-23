from django.utils.translation import ugettext as _

from modeltranslation.translator import register, TranslationOptions

from models import Student, Group

@register(Student)
class StudentTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name')
    required_languages = ('uk', 'en', 'ru')

@register(Group)
class GroupTranslationOptions(TranslationOptions):
    fields = ('title',)
    required_languages = ('uk', 'en', 'ru')

