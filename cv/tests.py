from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from cv.views import show_cv  

class CvPageTest(TestCase):

    def test_root_url_resolves_to_cve_view(self):
        found = resolve('/cv/')  
        self.assertEqual(found.func, show_cv)
    
    def test_uses_cv_template(self):
        response = self.client.get('/cv/')
        self.assertTemplateUsed(response, 'cv/cv.html')
    
    def test_cv_returns_correct_html(self):
        request = HttpRequest()  
        response = show_cv(request)  
        html = response.content.decode('utf8')  
        self.assertTrue(html.strip().startswith('<html>'))  
        self.assertIn('<title>Zenith\'s Blog</title>', html)  
        self.assertIn('<h1 style="text-align: center;">William Matson</h1>', html)
        self.assertTrue(html.strip().endswith('</html>'))  