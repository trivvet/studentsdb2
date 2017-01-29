from modeltranslation.translator import translator, TranslationOptions
from models import Student

class NewsTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'middle_name')
    required_languages = ('uk', 'en', 'ru')

translator.register(Student, NewsTranslationOptions)
