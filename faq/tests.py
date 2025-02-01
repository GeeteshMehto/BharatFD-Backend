from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import FAQ

class FAQModelTest(TestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(
            question="What is your name?",
            answer="<p>My name is FAQ Bot.</p>"
        )

    def test_get_translated_question_english(self):
        self.assertEqual(self.faq.get_translated_question('en'), self.faq.question)

    def test_get_translated_question_hindi(self):
        hindi_question = self.faq.get_translated_question('hi')
        self.assertTrue(isinstance(hindi_question, str))
        self.assertNotEqual(hindi_question, "")

class FAQAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.faq = FAQ.objects.create(
            question="How are you?",
            answer="<p>I am fine.</p>"
        )

    def test_faq_api_default_language(self):
        response = self.client.get(reverse('faq-list-create'))
        self.assertEqual(response.status_code, 200)
        # Check that question is in English by default.
        self.assertEqual(response.data[0]['question'], self.faq.question)

    def test_faq_api_hindi_language(self):
        response = self.client.get(reverse('faq-list-create') + '?lang=hi')
        self.assertEqual(response.status_code, 200)
        hindi_question = self.faq.get_translated_question('hi')
        self.assertEqual(response.data[0]['question'], hindi_question)
