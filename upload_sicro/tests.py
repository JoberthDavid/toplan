from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from upload_sicro.views import home_page, upload_sicro


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Data-base sistema de custos</title>', html)
        self.assertTrue(html.endswith('</html>'))
        self.assertTemplateUsed(response, 'home_page.html')

    def test_root_url_resolves_to_upload_sicro_view(self):
        found = resolve('/upload_sicro/')
        self.assertEqual(found.func, upload_sicro)

    def test_upload_sicro_returns_correct_html(self):
        response = self.client.get('/upload_sicro/')
        html = response.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>upload SICRO</title>', html)
        self.assertTrue(html.endswith('</html>'))
        self.assertTemplateUsed(response, 'upload_sicro.html')
    
    def test_can_save_a_POST_request(self):
        response = self.client.post('/upload_sicro/', data={})