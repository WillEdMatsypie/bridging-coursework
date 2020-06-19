
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth.models import User

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
        self.assertTrue(html.strip().endswith('</html>'))  

class NavBarAuthTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def tearDown(self):
        self.user.delete()
    
    def test_nav_bar_no_auth(self):
        response = self.client.get('/') 
        html = response.content.decode('utf8')  
        self.assertIn('<a class="nav-link" href="/blog/">Blog</span></a>', html)  
        self.assertIn('<a class="nav-link" href="/cv/">CV</span></a>', html) 
        self.assertNotIn('<a href="/blog/drafts/" class="nav-link">Drafts</span></a>', html)  
        self.assertIn('<a href="/accounts/login/" class="nav-link">Login</a>', html)
        self.assertNotIn('<a href="/accounts/logout/" class="nav-link">Log out</a>', html)
    
    def test_nav_bar_auth(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/') 
        html = response.content.decode('utf8')  
        self.assertIn('<a class="nav-link" href="/blog/">Blog</span></a>', html)  
        self.assertIn('<a class="nav-link" href="/cv/">CV</span></a>', html) 
        self.assertIn('<a href="/blog/drafts/" class="nav-link">Drafts</span></a>', html)  
        self.assertNotIn('<a href="/accounts/login/" class="nav-link">Login</a>', html)
        self.assertIn('<a href="/accounts/logout/" class="nav-link">Log out</a>', html)
        self.client.logout()