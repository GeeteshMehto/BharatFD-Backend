from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator
from django.core.cache import cache
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)
translator = Translator()


class FAQ(models.Model):

    question = models.TextField()
    answer = RichTextField()


    question_hi = models.TextField(blank=True, null=True)
    question_bn = models.TextField(blank=True, null=True)
    question_ta = models.TextField(blank=True, null=True)
    question_te = models.TextField(blank=True, null=True)
    question_ml = models.TextField(blank=True, null=True)
    question_gu = models.TextField(blank=True, null=True)
    question_kn = models.TextField(blank=True, null=True)
    question_mr = models.TextField(blank=True, null=True)
    question_pa = models.TextField(blank=True, null=True)
    question_or = models.TextField(blank=True, null=True)

    answer_hi = RichTextField(blank=True, null=True)
    answer_bn = RichTextField(blank=True, null=True)
    answer_ta = RichTextField(blank=True, null=True)
    answer_te = RichTextField(blank=True, null=True)
    answer_ml = RichTextField(blank=True, null=True)
    answer_gu = RichTextField(blank=True, null=True)
    answer_kn = RichTextField(blank=True, null=True)
    answer_mr = RichTextField(blank=True, null=True)
    answer_pa = RichTextField(blank=True, null=True)
    answer_or = RichTextField(blank=True, null=True)

    SUPPORTED_LANGUAGES = {
        'hi': ('question_hi', 'answer_hi'),
        'bn': ('question_bn', 'answer_bn'),
        'ta': ('question_ta', 'answer_ta'),
        'te': ('question_te', 'answer_te'),
        'ml': ('question_ml', 'answer_ml'),
        'gu': ('question_gu', 'answer_gu'),
        'kn': ('question_kn', 'answer_kn'),
        'mr': ('question_mr', 'answer_mr'),
        'pa': ('question_pa', 'answer_pa'),
        'or': ('question_or', 'answer_or'),
    }

    def clear_translation_cache(self):
        """Clear all cached translations for this FAQ"""
        for lang in self.SUPPORTED_LANGUAGES.keys():
            cache.delete(f"faq_{self.pk}_question_{lang}")
            cache.delete(f"faq_{self.pk}_answer_{lang}")

    def update_translations(self):
        """Update translations for all supported languages"""
        try:
            # Get the original values from the database if this is an update
            if self.pk:
                original = FAQ.objects.get(pk=self.pk)
                question_changed = original.question != self.question
                answer_changed = original.answer != self.answer
            else:
                question_changed = answer_changed = True

            for lang, (question_field, answer_field) in self.SUPPORTED_LANGUAGES.items():
                # Update question translation if the English question changed
                if question_changed:
                    self.translate_and_save_field(lang, question_field, self.question)

                # Update answer translation if the English answer changed
                if answer_changed:
                    self.translate_and_save_field(lang, answer_field, self.answer, is_rich_text=True)

            # Clear cache after updating translations
            if question_changed or answer_changed:
                self.clear_translation_cache()

        except Exception as e:
            logger.error(f"Error updating translations: {e}")

    def save(self, *args, **kwargs):
        """Override save() to update translations when English content changes"""
        # If this is a new instance or English content has changed, update translations
        self.update_translations()
        super().save(*args, **kwargs)


    def get_translated_question(self, lang='en'):

        if lang == 'en':
            return self.question

        field_name = self.SUPPORTED_LANGUAGES.get(lang, (None,))[0]
        if not field_name:
            return self.question

        cache_key = f"faq_{self.pk}_question_{lang}"
        translated_question = cache.get(cache_key)
        if translated_question:
            return translated_question

        translated_question = getattr(self, field_name) or self.translate_text(self.question, dest=lang)
        cache.set(cache_key, translated_question, timeout=3600)
        return translated_question

    def get_translated_answer(self, lang='en'):

        if lang == 'en':
            return self.answer

        field_name = self.SUPPORTED_LANGUAGES.get(lang, (None, None))[1]
        if not field_name:
            return self.answer

        cache_key = f"faq_{self.pk}_answer_{lang}"
        translated_answer = cache.get(cache_key)
        if translated_answer:
            return translated_answer

        translated_answer = getattr(self, field_name) or self.translate_rich_text(self.answer, dest=lang)
        cache.set(cache_key, translated_answer, timeout=3600)
        return translated_answer

    def translate_text(self, text, dest='hi'):

        try:
            translator = Translator()
            translated = translator.translate(text, dest=dest)
            return translated.text
        except Exception as e:
            logger.error(f"Error translating text: {e}")
            return text

    def translate_rich_text(self, text, dest='hi'):

        try:
            translator = Translator()
            soup = BeautifulSoup(text, 'html.parser')
            for tag in soup.find_all(string=True):
                if tag.strip():
                    logger.debug(f"Translating text: {tag}")
                    translated_text = translator.translate(tag, dest=dest).text
                    tag.replace_with(translated_text)
            return str(soup)
        except Exception as e:
            logger.error(f"Error translating RichTextField: {e}")
            return text

    def translate_and_save_field(self, lang, field_name, text, is_rich_text=False):

        translated_text = self.translate_text(text, dest=lang) if not is_rich_text else self.translate_rich_text(text,
                                                                                                                 dest=lang)
        setattr(self, field_name, translated_text)

    def __str__(self):
        return self.question[:50]