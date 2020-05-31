from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth.models import User

from cv.views import show_cv, education_new  
from cv.models import Education, Skill  
from .forms import EducationForm, SkillForm

class CvPageTest(TestCase):
    
    def test_root_url_resolves_to_cv_view(self):
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

class SkillModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def test_saving_and_retrieving_skill(self):
        first_item = Skill()
        first_item.title = "Skill 1"
        first_item.skill_type = "technical"
        first_item.save()


        second_item = Skill()
        second_item.title = "Skill 2"
        second_item.skill_type = "other"
        second_item.save()
        
        saved_items = Skill.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.title, 'Skill 1')
        self.assertEqual(second_saved_item.title, 'Skill 2')

    def test_url_resolves_to_skill_form_view(self):
        found = resolve('/cv/skill/new/')  
        self.assertEqual(found.func, skill_new)
    
    def test_uses_skill_form_template(self):
        response = self.client.get('/cv/skill/new/')
        self.assertTemplateUsed(response, 'cv/skill_edit.html')

    def test_skill_form_returns_correct_html(self):
        request = HttpRequest()  
        request.user = self.user
        response = skill_new(request)  
        html = response.content.decode('utf8')  
        self.assertTrue(html.strip().startswith('<html>'))  
        self.assertIn('<title>Zenith\'s Blog</title>', html)  
        self.assertIn('<h2>New Skill</h2>', html)
        self.assertTrue(html.strip().endswith('</html>'))  
    
    def test_view_skill_form(self):
        response = self.client.get('/cv/skill/new/')
        self.assertIsInstance(response.context['form'], SkillForm) 
        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'name="skill_type')

    def test_can_save_POST_request_to_education_model(self):
        data={'title':"Skill 3", 'skill_type':"technical",}
        response = self.client.post('/cv/skill/new/', data)
        self.assertEqual(Education.objects.count(), 1)
        new_item = Skill.objects.first()
        self.assertEqual(new_item.title, "Skill 3")
        self.assertEqual(new_item.skill_type, "technical")
    
    def test_redirect_after_POST_submission(self):
        data={'title':"Skill 4", 'skill_type':"other",}
        response = self.client.post('/cv/skill/new/', data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], "/cv/")
    
    def test_error_response_on_incomplete_form(self):
        data={'title':"", 'skill_type':"",}
        response = self.client.post('/cv/skill/new/', data)
        self.assertEqual(Skill.objects.count(), 0) # Doesn't add to DB
        self.assertTemplateUsed(response, 'cv/skill_edit.html') # Redirects to same page
    
    def test_bad_request(self):
        data={'title':"Oops",}
        response = self.client.post('cv/skill_edit.html', data)
        self.assertEqual(Education.objects.count(), 0) #Doesn't add to database
        
    def test_skill_deletion(self):
        data={'title':"Skill 6", 'skill_type':"technical",}
        self.client.post('/cv/skill/new/', data)
        self.assertEqual(Skill.objects.count(), 1)
        new_item = Skill.objects.first()
        new_item.delete()
        self.assertEqual(Skill.objects.count(), 0)
    
    def test_skill_deletion_url(self):
        data={'title':"Skill 7", 'skill_type':"other",}
        self.client.post('/cv/skill/new/', data)
        self.assertEqual(Skill.objects.count(), 1)
        new_item = Skill.objects.first()
        url = "/cv/skill/" + str(new_item.pk) + "/remove/"
        response = self.client.get(url)
        self.assertEqual(Skill.objects.count(), 0)
        self.assertEqual(response['location'], "/cv/")

class EducationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def test_saving_and_retrieving_education(self):
        first_item = Education()
        first_item.title = "Test Education 1"
        first_item.location = "Institution 1"
        first_item.start_date = "Test 01"
        first_item.end_date = "Test 10"
        first_item.brief_text = "Test 1 Brief" 
        first_item.detailed_text = "Test 1 Detailed" 
        first_item.save()


        second_item = Education()
        second_item.title = "Test Education 2"
        second_item.location = "Institution 2"
        second_item.start_date = "Test 02"
        second_item.end_date = "Test 20"
        second_item.brief_text = "Test 2 Brief" 
        second_item.detailed_text = "Test 2 Detailed" 
        second_item.save()
        

        saved_items = Education.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.title, 'Test Education 1')
        self.assertEqual(second_saved_item.title, 'Test Education 2')

    def test_url_resolves_to_education_form_view(self):
        found = resolve('/cv/education/new/')  
        self.assertEqual(found.func, education_new)
    
    def test_uses_education_form_template(self):
        response = self.client.get('/cv/education/new/')
        self.assertTemplateUsed(response, 'cv/education_edit.html')

    def test_education_form_returns_correct_html(self):
        request = HttpRequest()  
        request.user = self.user
        response = education_new(request)  
        html = response.content.decode('utf8')  
        self.assertTrue(html.strip().startswith('<html>'))  
        self.assertIn('<title>Zenith\'s Blog</title>', html)  
        self.assertIn('<h2>New Education</h2>', html)
        self.assertTrue(html.strip().endswith('</html>'))  
    
    def test_view_education_form(self):
        response = self.client.get('/cv/education/new/')
        self.assertIsInstance(response.context['form'], EducationForm) 
        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'name="location"')
        self.assertContains(response, 'name="start_date"')
        self.assertContains(response, 'name="end_date"')
        self.assertContains(response, 'name="brief_text"')
        self.assertContains(response, 'name="detailed_text"')

    def test_can_save_POST_request_to_education_model(self):
        data={'title':"Test Education 3", 'location':"Institution 3", 'start_date':"Test 03", 'end_date':"Test 30", 'brief_text':"Test 3 Brief", 'detailed_text':"Test 3 Detailed",}
        response = self.client.post('/cv/education/new/', data)
        self.assertEqual(Education.objects.count(), 1)
        new_item = Education.objects.first()
        self.assertEqual(new_item.title, "Test Education 3")
        self.assertEqual(new_item.brief_text, "Test 3 Brief")
    
    def test_redirect_after_POST_submission(self):
        data={'title':"Test Education 4", 'location':"Institution 4", 'start_date':"Test 04", 'end_date':"Test 40", 'brief_text':"Test 4 Brief", 'detailed_text':"Test 4 Detailed",}
        response = self.client.post('/cv/education/new/', data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], "/cv/")
    
    def test_error_response_on_incomplete_form(self):
        data={'title':"Test Blank Dates", 'location':"Institution 5", 'start_date':"", 'end_date':"", 'brief_text':"Test 5 Brief", 'detailed_text':"Test 5 Detailed",}
        response = self.client.post('/cv/education/new/', data)
        self.assertEqual(Education.objects.count(), 0) # Doesn't add to DB
        self.assertTemplateUsed(response, 'cv/education_edit.html') # Redirects to same page
    
    def test_bad_request(self):
        data={'title':"Test no text", 'location':"Institution 5", 'start_date':"", 'end_date':"",}
        response = self.client.post('cv/education_edit.html', data)
        self.assertEqual(Education.objects.count(), 0) #Doesn't add to database
        
    def test_education_deletion(self):
        data={'title':"Test Education 6", 'location':"Institution 6", 'start_date':"Test 06", 'end_date':"Test 60", 'brief_text':"Test 6 Brief", 'detailed_text':"Test 6 Detailed",}
        self.client.post('/cv/education/new/', data)
        self.assertEqual(Education.objects.count(), 1)
        new_item = Education.objects.first()
        new_item.delete()
        self.assertEqual(Education.objects.count(), 0)
    
    def test_education_deletion_url(self):
        data={'title':"Test Education 7", 'location':"Institution 7", 'start_date':"Test 07", 'end_date':"Test 70", 'brief_text':"Test 7 Brief", 'detailed_text':"Test 7 Detailed",}
        self.client.post('/cv/education/new/', data)
        self.assertEqual(Education.objects.count(), 1)
        new_item = Education.objects.first()
        url = "/cv/education/" + str(new_item.pk) + "/remove/"
        response = self.client.get(url)
        self.assertEqual(Education.objects.count(), 0)
        self.assertEqual(response['location'], "/cv/")