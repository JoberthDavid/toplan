from operator import contains
from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from upload_app.forms import FormFileCost
from upload_app.views import home_page, upload_app
from upload_app.models import ModelFileCost

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
        self.assertIn('<title>API de custos</title>', html)
        self.assertTrue(html.endswith('</html>'))

    
class UploadAppTest(TestCase):

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
        self.assertIn('enctype="multipart/form-data', html)
        self.assertIn('<title>Carregar arquivo</title>', html)
        self.assertTrue(html.endswith('</html>'))

    def test_can_save_a_POST_request(self):
        response = self.client.post('/upload_app/', data={})
    
class ModelFileCostTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        ModelFileCost.objects.create(data_base='2014-04-01', file='./DF 04-2021 Relatório Analítico de ComposiçΣes de Custos.pdf')
    
    def test_get_absolute_url(self):
        file = ModelFileCost.objects.get(id=1)
        self.assertEqual(file.get_absolute_url(), '/upload_app/1/')

    def test_methodology_label(self):
        file = ModelFileCost.objects.get(id=1)
        field_label = file._meta.get_field('methodology').verbose_name
        self.assertEqual(field_label, 'Metodologia')

class FormFileCostTest(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        ModelFileCost.objects.create(data_base='2014-04-01', file='./DF 04-2021 Relatório Analítico de ComposiçΣes de Custos.pdf')
    

    def test_valid_form(self):
        file = ModelFileCost.objects.get(id=1)
        data = {'methodology':file.methodology,
                'data_base': file.data_base,
                'uf': file.uf,
                'type_system': file.type_system,
                'type_file': file.type_file,
                }
        data_file = {'file': file.file,}
        form = FormFileCost(data=data, files=data_file)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        file = ModelFileCost.objects.create(data_base='2014-04-01', file='')
        data = {'data_base': file.data_base,
                'file': file.file,
                }
        form = FormFileCost(data=data)
        self.assertFalse(form.is_valid())