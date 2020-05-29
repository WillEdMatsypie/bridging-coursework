
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from home.views import home  

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_view(self):
        found = resolve('/')  
        self.assertEqual(found.func, home)
    
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    
    def test_home_returns_correct_html(self):
        request = HttpRequest()  
        response = home(request)  
        html = response.content.decode('utf8')  
        self.assertTrue(html.strip().startswith('<html>'))  
        self.assertIn('<title>Zenith\'s Blog</title>', html)  
        self.assertIn('<h1>Zenith</h1>', html)
        self.assertTrue(html.endswith('</html>'))  