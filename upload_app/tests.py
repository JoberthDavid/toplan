from operator import contains
from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from upload_app.views import home_page, upload_app


class HomePageTest(TestCase):

    def setUp(self):
        """Must setUp response_home_page and response_upload_app"""
        self.response_home_page = self.client.get('/')
        self.response_upload_app = self.client.get('/upload_app/')


    def test_root_url_resolves_to_home_page_view(self):
        """Must return status code 200"""
        found = resolve('/')
        self.assertEqual(found.func, home_page)
        self.assertEqual(200, self.response_home_page.status_code)

    def test_home_page_returns_correct_html(self):
        """Must use home_page.html"""
        self.assertTemplateUsed(self.response_home_page, 'home_page.html')
        
    def test_home_page_basic_html_contents(self):
        """Must return basic html contents home_page"""
        html = self.response_home_page.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>Data-base sistema de custos</title>', html)
        self.assertTrue(html.endswith('</html>'))

    
class UploadSicroTest(TestCase):

    def setUp(self):
        """Must setUp response_upload_app"""
        self.response_upload_app = self.client.get('/upload_app/')
    
    def test_root_url_resolves_to_upload_app_view(self):
        """Must return status code 200"""
        found = resolve('/upload_app/')
        self.assertEqual(found.func, upload_app)
        self.assertEqual(200, self.response_upload_app.status_code)

    def test_upload_app_returns_correct_html(self):
        """Must use home_page.html"""
        self.assertTemplateUsed(self.response_upload_app, 'upload_app.html')

    def test_upload_app_basic_html_contents(self):
        """Must return basic html contents upload_app"""
        html = self.response_upload_app.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>upload SICRO</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_can_save_a_POST_request(self):
        response = self.client.post('/upload_app/', data={})