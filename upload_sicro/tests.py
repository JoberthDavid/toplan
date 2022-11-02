from operator import contains
from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from upload_sicro.views import home_page, upload_sicro


class HomePageTest(TestCase):

    def setUp(self):
        """Must setUp response_home_page and response_upload_sicro"""
        self.response_home_page = self.client.get('/')
        self.response_upload_sicro = self.client.get('/upload_sicro/')


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
        """Must setUp response_upload_sicro"""
        self.response_upload_sicro = self.client.get('/upload_sicro/')
    
    def test_root_url_resolves_to_upload_sicro_view(self):
        """Must return status code 200"""
        found = resolve('/upload_sicro/')
        self.assertEqual(found.func, upload_sicro)
        self.assertEqual(200, self.response_upload_sicro.status_code)

    def test_upload_sicro_returns_correct_html(self):
        """Must use home_page.html"""
        self.assertTemplateUsed(self.response_upload_sicro, 'upload_sicro.html')

    def test_upload_sicro_basic_html_contents(self):
        """Must return basic html contents upload_sicro"""
        html = self.response_upload_sicro.content.decode('utf8')
        self.assertTrue(html.startswith('<!DOCTYPE html>'))
        self.assertIn('<title>upload SICRO</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_can_save_a_POST_request(self):
        response = self.client.post('/upload_sicro/', data={})