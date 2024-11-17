import json
from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse

class KnowledgeViewTest(TestCase):
    def test_add_to_knowledge(self):
        url = reverse('knowledge_view')
        data = {
            'pageTitle': 'Test Title',
            'text': 'Test text content',
            'pageUrl': 'http://example.com'
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'data added to index')

    def test_get_knowledge(self):
        url = reverse('knowledge_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response, JsonResponse)
        self.assertIn('data', response.json())