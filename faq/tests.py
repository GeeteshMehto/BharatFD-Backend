from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from bs4 import BeautifulSoup
from django.core.cache import cache
from .models import FAQ


class FAQModelTests(TestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(
            question="What is Django?",
            answer="<p>Django is a high-level Python web framework.</p>"
        )

    def test_faq_creation(self):
        self.assertEqual(FAQ.objects.count(), 1)
        self.assertEqual(self.faq.question, "What is Django?")
        self.assertEqual(self.faq.answer, "<p>Django is a high-level Python web framework.</p>")

    def test_str_representation(self):
        long_question_faq = FAQ.objects.create(
            question="A" * 100,
            answer="Test Answer"
        )
        self.assertEqual(str(long_question_faq), "A" * 50)

    def test_translation_cache_clearing(self):
        cache.set(f"faq_{self.faq.pk}_question_hi", "Test Hindi Question")
        cache.set(f"faq_{self.faq.pk}_answer_hi", "Test Hindi Answer")

        self.faq.clear_translation_cache()

        self.assertIsNone(cache.get(f"faq_{self.faq.pk}_question_hi"))
        self.assertIsNone(cache.get(f"faq_{self.faq.pk}_answer_hi"))

    def test_get_translated_question(self):
        # Test English (default)
        self.assertEqual(self.faq.get_translated_question(), "What is Django?")

        # Test supported language
        self.faq.question_hi = "Django क्या है?"
        self.faq.save()
        self.assertEqual(self.faq.get_translated_question('hi'), "Django क्या है?")

    def test_get_translated_answer(self):
        # Test English (default)
        self.assertEqual(
            self.faq.get_translated_answer(),
            "<p>Django is a high-level Python web framework.</p>"
        )

        # Test supported language
        self.faq.answer_hi = "<p>Django एक उच्च-स्तरीय Python वेब फ्रेमवर्क है।</p>"
        self.faq.save()
        self.assertEqual(
            self.faq.get_translated_answer('hi'),
            "<p>Django एक उच्च-स्तरीय Python वेब फ्रेमवर्क है।</p>"
        )


class FAQAPITests(APITestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(
            question="What is Django?",
            answer="<p>Django is a high-level Python web framework.</p>"
        )
        self.list_url = reverse('faq-list-create')
        self.detail_url = reverse('faq-detail', kwargs={'pk': self.faq.pk})

    def test_create_faq(self):
        data = {
            'question': 'API Test Question',
            'answer': '<p>API Test Answer</p>'
        }

        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FAQ.objects.count(), 2)
        self.assertEqual(FAQ.objects.last().question, 'API Test Question')

    def test_list_faqs(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question'], self.faq.question)

    def test_list_faqs_with_language(self):
        self.faq.question_hi = "हिंदी प्रश्न"
        self.faq.answer_hi = "<p>हिंदी उत्तर</p>"
        self.faq.save()

        response = self.client.get(f"{self.list_url}?lang=hi")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['question'], "हिंदी प्रश्न")
        self.assertEqual(response.data[0]['answer'], "<p>हिंदी उत्तर</p>")

    def test_retrieve_faq(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question'], self.faq.question)

    def test_update_faq(self):
        data = {
            'question': 'Updated Question',
            'answer': '<p>Updated Answer</p>'
        }

        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.faq.refresh_from_db()
        self.assertEqual(self.faq.question, 'Updated Question')
        self.assertEqual(self.faq.answer, '<p>Updated Answer</p>')

    def test_delete_faq(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FAQ.objects.count(), 0)


class FAQTranslationTests(TestCase):
    def test_translation_on_create(self):
        faq = FAQ.objects.create(
            question="How are you?",
            answer="<p>I am fine.</p>"
        )
        # Translation should be triggered on creation
        self.assertIsNotNone(faq.question_hi)
        self.assertIsNotNone(faq.answer_hi)

    def test_translation_on_update(self):
        faq = FAQ.objects.create(
            question="Initial question",
            answer="<p>Initial answer</p>"
        )
        original_hi_question = faq.question_hi

        faq.question = "Updated question"
        faq.save()

        faq.refresh_from_db()
        self.assertNotEqual(faq.question_hi, original_hi_question)

    def test_html_preservation_in_translation(self):
        faq = FAQ.objects.create(
            question="Test",
            answer="<p><strong>Bold</strong> and <em>italic</em> text</p>"
        )

        soup = BeautifulSoup(faq.answer_hi, 'html.parser')
        self.assertIsNotNone(soup.find('strong'))
        self.assertIsNotNone(soup.find('em'))