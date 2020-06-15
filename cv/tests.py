from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth.models import User

from cv.views import show_cv, education_new, education_edit, skill_new, skill_edit, experience_new, experience_edit, interest_new, interest_edit
from cv.models import Education, Skill, Experience, Interest  
from .forms import EducationForm, SkillForm, ExperienceForm, InterestForm

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

    def test_can_save_POST_request_to_skill_model(self):
        data={'title':"Skill 3", 'skill_type':"technical",}
        response = self.client.post('/cv/skill/new/', data)
        self.assertEqual(Skill.objects.count(), 1)
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
        response = self.client.post('/cv/skill/new/', data)
        self.assertEqual(Skill.objects.count(), 0) #Doesn't add to database
        
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

    def setup_edit(self, data):
        self.client.post('/cv/skill/new/', data)
        self.assertEqual(Skill.objects.count(), 1)
        new_item = Skill.objects.first()
        return "/cv/skill/" + str(new_item.pk) + "/edit/"

    def test_skill_edit(self):
        data={'title':"Skill 8", 'skill_type':"other",}
        url = self.setup_edit(data)
        data2={'title':"Skill 80", 'skill_type':"technical",}
        response = self.client.post(url, data2)
        self.assertEqual(Skill.objects.count(), 1)
        self.assertEqual(response['location'], "/cv/")
        edited_item = Skill.objects.first()
        self.assertEqual(edited_item.title, "Skill 80")
        self.assertEqual(edited_item.skill_type, "technical")
    
    def test_skill_edit_404(self):
        data={'title':"Skill 9", 'skill_type':"other",}
        url = "/cv/skill/" + str(1) + "/edit/"
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Skill.objects.count(), 0)
    
    def test_url_resolves_to_skill_form_edit_view(self):
        data={'title':"Skill 10", 'skill_type':"technical",}
        url = self.setup_edit(data)
        found = resolve(url)  
        self.assertEqual(found.func, skill_edit)
    
    def test_uses_skill_form_edit_template(self):
        data={'title':"Skill 11", 'skill_type':"technical",}
        url = self.setup_edit(data)
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'cv/skill_edit.html')
    
    def test_view_skill_edit_form(self):
        data={'title':"Skill 12", 'skill_type':"technical",}
        url = self.setup_edit(data)
        response = self.client.get(url)
        self.assertIsInstance(response.context['form'], SkillForm) 
        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'name="skill_type')

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
        data={'title':"Test no text", 'location':"Institution 5", 'start_date':"Date 1", 'end_date':"Date 2",}
        response = self.client.post('/cv/education/new/', data)
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

    def setup_edit(self, data):
        self.client.post('/cv/education/new/', data)
        self.assertEqual(Education.objects.count(), 1)
        new_item = Education.objects.first()
        return "/cv/education/" + str(new_item.pk) + "/edit/"

    def test_education_edit(self):
        data={'title':"Test Education 8", 'location':"Institution 8", 'start_date':"Test 08", 'end_date':"Test 80", 'brief_text':"Test 8 Brief", 'detailed_text':"Test 8 Detailed",}
        url = self.setup_edit(data)
        data2={'title':"Test Education 8", 'location':"Institution 80", 'start_date':"Test 08", 'end_date':"Test 80", 'brief_text':"Test 8 Brief", 'detailed_text':"Test 808 Detailed",}
        response = self.client.post(url, data2)
        self.assertEqual(Education.objects.count(), 1)
        self.assertEqual(response['location'], "/cv/")
        edited_item = Education.objects.first()
        self.assertEqual(edited_item.title, "Test Education 8")
        self.assertEqual(edited_item.location, "Institution 80")
        self.assertEqual(edited_item.detailed_text, "Test 808 Detailed")
    
    def test_education_edit_404(self):
        data={'title':"Test Education 9", 'location':"Institution 9", 'start_date':"Test 09", 'end_date':"Test 90", 'brief_text':"Test 9 Brief", 'detailed_text':"Test 9 Detailed",}
        url = "/cv/education/" + str(1) + "/edit/"
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Education.objects.count(), 0)
    
    def test_url_resolves_to_education_form_edit_view(self):
        data={'title':"Test Education 10", 'location':"Institution 10", 'start_date':"Test 010", 'end_date':"Test 100", 'brief_text':"Test 10 Brief", 'detailed_text':"Test 10 Detailed",}
        url = self.setup_edit(data)
        found = resolve(url)  
        self.assertEqual(found.func, education_edit)
    
    def test_uses_education_form_edit_template(self):
        data={'title':"Test Education 11", 'location':"Institution 11", 'start_date':"Test 011", 'end_date':"Test 110", 'brief_text':"Test 11 Brief", 'detailed_text':"Test 11 Detailed",}
        url = self.setup_edit(data)
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'cv/education_edit.html')
    
    def test_view_education_edit_form(self):
        data={'title':"Test Education 12", 'location':"Institution 12", 'start_date':"Test 012", 'end_date':"Test 120", 'brief_text':"Test 12 Brief", 'detailed_text':"Test 12 Detailed",}
        url = self.setup_edit(data)
        response = self.client.get(url)
        self.assertIsInstance(response.context['form'], EducationForm) 
        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'name="location"')
        self.assertContains(response, 'name="start_date"')
        self.assertContains(response, 'name="end_date"')
        self.assertContains(response, 'name="brief_text"')
        self.assertContains(response, 'name="detailed_text"')

class ExperienceModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def test_saving_and_retrieving_experience(self):
        first_item = Experience()
        first_item.title = "Test Experience 1"
        first_item.subtitle = "Experience 1 Type"
        first_item.date = "Test 01"
        first_item.text = "Test 1 Detailed" 
        first_item.save()


        second_item = Experience()
        second_item.title = "Test Experience 2"
        second_item.subtitle = "Experience 2 Type"
        second_item.date = "Test 02"
        second_item.text = "Test 2 Detailed" 
        second_item.save()
        

        saved_items = Experience.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.title, 'Test Experience 1')
        self.assertEqual(second_saved_item.title, 'Test Experience 2')

    def test_url_resolves_to_experience_form_view(self):
        found = resolve('/cv/experience/new/')  
        self.assertEqual(found.func, experience_new)
    
    def test_uses_experience_form_template(self):
        response = self.client.get('/cv/experience/new/')
        self.assertTemplateUsed(response, 'cv/experience_edit.html')

    def test_experience_form_returns_correct_html(self):
        request = HttpRequest()  
        request.user = self.user
        response = experience_new(request)  
        html = response.content.decode('utf8')  
        self.assertTrue(html.strip().startswith('<html>'))  
        self.assertIn('<title>Zenith\'s Blog</title>', html)  
        self.assertIn('<h2>New Experience</h2>', html)
        self.assertTrue(html.strip().endswith('</html>'))  
    
    def test_view_experience_form(self):
        response = self.client.get('/cv/experience/new/')
        self.assertIsInstance(response.context['form'], ExperienceForm) 
        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'name="subtitle"')
        self.assertContains(response, 'name="date"')
        self.assertContains(response, 'name="text"')

    def test_can_save_POST_request_to_experience_model(self):
        data={'title':"Test Experience 3", 'subtitle':"Experience Type 3", 'date':"Test 03", 'text':"Test 3 Detailed",}
        response = self.client.post('/cv/experience/new/', data)
        self.assertEqual(Experience.objects.count(), 1)
        new_item = Experience.objects.first()
        self.assertEqual(new_item.title, "Test Experience 3")
        self.assertEqual(new_item.text, "Test 3 Detailed")
    
    def test_redirect_after_POST_submission(self):
        data={'title':"Test Experience 4", 'subtitle':"Experience Type 4", 'date':"Test 04", 'text':"Test 4 Detailed",}
        response = self.client.post('/cv/experience/new/', data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], "/cv/")
    
    def test_error_response_on_incomplete_form(self):
        data={'title':"Test Blank Date", 'subtitle':"Experience Type 5", 'date':"", 'text':"Test 5 Detailed",}
        response = self.client.post('/cv/experience/new/', data)
        self.assertEqual(Experience.objects.count(), 0) # Doesn't add to DB
        self.assertTemplateUsed(response, 'cv/experience_edit.html') # Redirects to same page
    
    def test_bad_request(self):
        data={'title':"Test no text", 'location':"Institution 5", 'date':"Date 1"}
        response = self.client.post('/cv/experience/new/', data)
        self.assertEqual(Experience.objects.count(), 0) #Doesn't add to database
        
    def test_experience_deletion(self):
        data={'title':"Test Experience 6", 'subtitle':"Experience Type 6", 'date':"Test 06", 'text':"Test 6 Detailed",}
        self.client.post('/cv/experience/new/', data)
        self.assertEqual(Experience.objects.count(), 1)
        new_item = Experience.objects.first()
        new_item.delete()
        self.assertEqual(Experience.objects.count(), 0)
    
    def test_experience_deletion_url(self):
        data={'title':"Test Experience 7", 'subtitle':"Experience Type 7", 'date':"Test 07", 'text':"Test 7 Detailed",}
        self.client.post('/cv/experience/new/', data)
        self.assertEqual(Experience.objects.count(), 1)
        new_item = Experience.objects.first()
        url = "/cv/experience/" + str(new_item.pk) + "/remove/"
        response = self.client.get(url)
        self.assertEqual(Experience.objects.count(), 0)
        self.assertEqual(response['location'], "/cv/")

    def setup_edit(self, data):
        self.client.post('/cv/experience/new/', data)
        self.assertEqual(Experience.objects.count(), 1)
        new_item = Experience.objects.first()
        return "/cv/experience/" + str(new_item.pk) + "/edit/"

    def test_experience_edit(self):
        data={'title':"Test Experience 8", 'subtitle':"Experience Type 8", 'date':"Test 08", 'text':"Test 8 Detailed",}
        url = self.setup_edit(data)
        data2={'title':"Test Experience 8", 'subtitle':"Experience Type 80", 'date':"Test 08", 'text':"Test 80 Detailed",}
        response = self.client.post(url, data2)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertEqual(response['location'], "/cv/")
        edited_item = Experience.objects.first()
        self.assertEqual(edited_item.title, "Test Experience 8")
        self.assertEqual(edited_item.subtitle, "Experience Type 80")
        self.assertEqual(edited_item.text, "Test 80 Detailed")
    
    def test_experience_edit_404(self):
        data={'title':"Test Experience 9", 'subtitle':"Experience Type 9", 'date':"Test 09", 'text':"Test 9 Detailed",}
        url = "/cv/experience/" + str(1) + "/edit/"
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Experience.objects.count(), 0)
    
    def test_url_resolves_to_experience_form_edit_view(self):
        data={'title':"Test Experience 10", 'subtitle':"Experience Type 10", 'date':"Test 010", 'text':"Test 10 Detailed",}
        url = self.setup_edit(data)
        found = resolve(url)  
        self.assertEqual(found.func, experience_edit)
    
    def test_uses_experience_form_edit_template(self):
        data={'title':"Test Experience 11", 'subtitle':"Experience Type 11", 'date':"Test 011", 'text':"Test 11 Detailed",}
        url = self.setup_edit(data)
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'cv/experience_edit.html')
    
    def test_view_experience_edit_form(self):
        data={'title':"Test Experience 12", 'subtitle':"Experience Type 12", 'date':"Test 012", 'text':"Test 12 Detailed",}
        url = self.setup_edit(data)
        response = self.client.get(url)
        self.assertIsInstance(response.context['form'], ExperienceForm) 
        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'name="subtitle"')
        self.assertContains(response, 'name="date"')
        self.assertContains(response, 'name="text"')

class InterestModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def test_saving_and_retrieving_interest(self):
        first_item = Interest()
        first_item.title = "Test Interest 1"
        first_item.save()

        second_item = Interest()
        second_item.title = "Test Interest 2"
        second_item.save()
        
        saved_items = Interest.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.title, 'Test Interest 1')
        self.assertEqual(second_saved_item.title, 'Test Interest 2')

    def test_url_resolves_to_interest_form_view(self):
        found = resolve('/cv/interest/new/')  
        self.assertEqual(found.func, interest_new)
    
    def test_uses_interest_form_template(self):
        response = self.client.get('/cv/interest/new/')
        self.assertTemplateUsed(response, 'cv/interest_edit.html')

    def test_interest_form_returns_correct_html(self):
        request = HttpRequest()  
        request.user = self.user
        response = interest_new(request)  
        html = response.content.decode('utf8')  
        self.assertTrue(html.strip().startswith('<html>'))  
        self.assertIn('<title>Zenith\'s Blog</title>', html)  
        self.assertIn('<h2>New Interest</h2>', html)
        self.assertTrue(html.strip().endswith('</html>'))  
    
    def test_view_interest_form(self):
        response = self.client.get('/cv/interest/new/')
        self.assertIsInstance(response.context['form'], InterestForm) 
        self.assertContains(response, 'name="title"')

    def test_can_save_POST_request_to_interest_model(self):
        data={'title':"Test Interest 3",}
        response = self.client.post('/cv/interest/new/', data)
        self.assertEqual(Interest.objects.count(), 1)
        new_item = Interest.objects.first()
        self.assertEqual(new_item.title, "Test Interest 3")
    
    def test_redirect_after_POST_submission(self):
        data={'title':"Test Interest 4",}
        response = self.client.post('/cv/interest/new/', data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], "/cv/")
    
    def test_error_response_on_incomplete_form(self):
        data={'title':"",}
        response = self.client.post('/cv/interest/new/', data)
        self.assertEqual(Interest.objects.count(), 0) # Doesn't add to DB
        self.assertTemplateUsed(response, 'cv/interest_edit.html') # Redirects to same page
    
    def test_bad_request(self):
        data={}
        response = self.client.post('/cv/interest/new/', data)
        self.assertEqual(Interest.objects.count(), 0) #Doesn't add to database
        
    def test_interest_deletion(self):
        data={'title':"Test Interest 6",}
        self.client.post('/cv/interest/new/', data)
        self.assertEqual(Interest.objects.count(), 1)
        new_item = Interest.objects.first()
        new_item.delete()
        self.assertEqual(Interest.objects.count(), 0)
    
    def test_interest_deletion_url(self):
        data={'title':"Test Interest 7",}
        self.client.post('/cv/interest/new/', data)
        self.assertEqual(Interest.objects.count(), 1)
        new_item = Interest.objects.first()
        url = "/cv/interest/" + str(new_item.pk) + "/remove/"
        response = self.client.get(url)
        self.assertEqual(Interest.objects.count(), 0)
        self.assertEqual(response['location'], "/cv/")
    
    def setup_edit(self, data):
        self.client.post('/cv/interest/new/', data)
        self.assertEqual(Interest.objects.count(), 1)
        new_item = Interest.objects.first()
        return "/cv/interest/" + str(new_item.pk) + "/edit/"

    def test_interest_edit(self):
        data={'title':"Test Interest 8",}
        url = self.setup_edit(data)
        data2={'title':"Test Interest 80",}
        response = self.client.post(url, data2)
        self.assertEqual(Interest.objects.count(), 1)
        self.assertEqual(response['location'], "/cv/")
        edited_item = Interest.objects.first()
        self.assertEqual(edited_item.title, "Test Interest 80")
    
    def test_interest_edit_404(self):
        data={'title':"Test Interest 9",}
        url = "/cv/interest/" + str(1) + "/edit/"
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Interest.objects.count(), 0)
    
    def test_url_resolves_to_interest_form_edit_view(self):
        data={'title':"Test Interest 11",}
        url = self.setup_edit(data)
        found = resolve(url)  
        self.assertEqual(found.func, interest_edit)
    
    def test_uses_interest_form_edit_template(self):
        data={'title':"Test Interest 12",}
        url = self.setup_edit(data)
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'cv/interest_edit.html')
    
    def test_view_interest_edit_form(self):
        data={'title':"Test Interest 13",}
        url = self.setup_edit(data)
        response = self.client.get(url)
        self.assertIsInstance(response.context['form'], InterestForm) 
        self.assertContains(response, 'name="title"')

class AuthenticationTest(TestCase):

    def test_new_interest_form_unauthenticated(self):
        response = self.client.get('/cv/interest/new/')
        self.assertNotEqual(response['location'], "/cv/interest/new/")
        self.assertEqual(response['location'], "/accounts/login/?next=/cv/interest/new/")
    
    def test_new_interest_post_unauthenticated(self):
        data={'title':"Test No Auth Interest",}
        response = self.client.post('/cv/interest/new/', data)
        self.assertEqual(Interest.objects.count(), 0)
        self.assertEqual(response['location'], "/accounts/login/?next=/cv/interest/new/")
    
    def test_edit_interest_form_unauthenticated(self):
        item = Interest()
        item.title = "Test No Auth Interest 1"
        item.save()
        self.assertEqual(Interest.objects.count(), 1)
        new_item = Interest.objects.first()
        url = "/cv/interest/" + str(new_item.pk) + "/edit/"
        response = self.client.get(url)
        self.assertEqual(Interest.objects.count(), 1)
        self.assertNotEqual(response['location'], url)
        self.assertEqual(response['location'], "/accounts/login/?next="+url)

    def test_edit_interest_post_unauthenticated(self):
        item = Interest()
        item.title = "Test No Auth Interest 2"
        item.save()
        self.assertEqual(Interest.objects.count(), 1)
        new_item = Interest.objects.first()
        url = "/cv/interest/" + str(new_item.pk) + "/edit/"
        data={'title':"Test No Auth Interest 20",}
        response = self.client.post(url, data)
        self.assertEqual(Interest.objects.count(), 1)
        self.assertNotEqual(response['location'], "/cv/")
        self.assertEqual(response['location'], "/accounts/login/?next="+url)
        unedited_item = Interest.objects.first()
        self.assertEqual(unedited_item.title, "Test No Auth Interest 2")
    
    def test_delete_interest_unauthenticated(self):
        item = Interest()
        item.title = "Test No Auth Interest 3"
        item.save()
        self.assertEqual(Interest.objects.count(), 1)
        new_item = Interest.objects.first()
        url = "/cv/interest/" + str(new_item.pk) + "/remove/"
        response = self.client.get(url)
        self.assertEqual(Interest.objects.count(), 1)
        self.assertNotEqual(response['location'], "/cv/")
        self.assertEqual(response['location'], "/accounts/login/?next="+url)
    
    def test_new_skill_form_unauthenticated(self):
        response = self.client.get('/cv/skill/new/')
        self.assertNotEqual(response['location'], "/cv/skill/new/")
        self.assertEqual(response['location'], "/accounts/login/?next=/cv/skill/new/")
    
    def test_new_skill_post_unauthenticated(self):
        data={'title':"Test No Auth Skill", 'skill_type':"technical"}
        response = self.client.post('/cv/skill/new/', data)
        self.assertEqual(Skill.objects.count(), 0)
        self.assertEqual(response['location'], "/accounts/login/?next=/cv/skill/new/")
    
    def test_edit_skill_form_unauthenticated(self):
        item = Skill()
        item.title = "Test No Auth Skill 1"
        item.skill_type = "technical"
        item.save()
        self.assertEqual(Skill.objects.count(), 1)
        new_item = Skill.objects.first()
        url = "/cv/skill/" + str(new_item.pk) + "/edit/"
        response = self.client.get(url)
        self.assertEqual(Skill.objects.count(), 1)
        self.assertNotEqual(response['location'], url)
        self.assertEqual(response['location'], "/accounts/login/?next="+url)

    def test_edit_skill_post_unauthenticated(self):
        item = Skill()
        item.title = "Test No Auth Skill 2"
        item.skill_type = "technical"
        item.save()
        self.assertEqual(Skill.objects.count(), 1)
        new_item = Skill.objects.first()
        url = "/cv/skill/" + str(new_item.pk) + "/edit/"
        data={'title':"Test No Auth Skill 20", 'skill_type':"other"}
        response = self.client.post(url, data)
        self.assertEqual(Skill.objects.count(), 1)
        self.assertNotEqual(response['location'], "/cv/")
        self.assertEqual(response['location'], "/accounts/login/?next="+url)
        unedited_item = Skill.objects.first()
        self.assertEqual(unedited_item.title, "Test No Auth Skill 2")
        self.assertEqual(unedited_item.skill_type, "technical")
    
    def test_delete_skill_unauthenticated(self):
        item = Skill()
        item.title = "Test No Auth Skill 3"
        item.skill_type = "technical"
        item.save()
        self.assertEqual(Skill.objects.count(), 1)
        new_item = Skill.objects.first()
        url = "/cv/skill/" + str(new_item.pk) + "/remove/"
        response = self.client.get(url)
        self.assertEqual(Skill.objects.count(), 1)
        self.assertNotEqual(response['location'], "/cv/")
        self.assertEqual(response['location'], "/accounts/login/?next="+url)
    
    def test_new_education_form_unauthenticated(self):
        response = self.client.get('/cv/education/new/')
        self.assertNotEqual(response['location'], "/cv/education/new/")
        self.assertEqual(response['location'], "/accounts/login/?next=/cv/education/new/")
    
    def test_new_education_post_unauthenticated(self):
        data={'title':"Test No Auth Education", 'location':"Institution", 'start_date':"Test date", 'end_date':"Test end", 'brief_text':"Test Brief", 'detailed_text':"Test Detailed",}
        response = self.client.post('/cv/education/new/', data)
        self.assertEqual(Education.objects.count(), 0)
        self.assertEqual(response['location'], "/accounts/login/?next=/cv/education/new/")
    
    def test_edit_education_form_unauthenticated(self):
        item = Education()
        item.title = "Test No Auth Education 1"
        item.location = "Institution No Auth 1"
        item.start_date = "Test No Auth 01"
        item.end_date = "Test No Auth 10"
        item.brief_text = "Test No Auth 1 Brief" 
        item.detailed_text = "Test No Auth 1 Detailed" 
        item.save()
        self.assertEqual(Education.objects.count(), 1)
        new_item = Education.objects.first()
        url = "/cv/education/" + str(new_item.pk) + "/edit/"
        response = self.client.get(url)
        self.assertEqual(Education.objects.count(), 1)
        self.assertNotEqual(response['location'], url)
        self.assertEqual(response['location'], "/accounts/login/?next="+url)

    def test_edit_education_post_unauthenticated(self):
        item = Education()
        item.title = "Test No Auth Education 2"
        item.location = "Institution No Auth 2"
        item.start_date = "Test No Auth 02"
        item.end_date = "Test No Auth 20"
        item.brief_text = "Test No Auth 2 Brief" 
        item.detailed_text = "Test No Auth 2 Detailed" 
        item.save()
        self.assertEqual(Education.objects.count(), 1)
        new_item = Education.objects.first()
        url = "/cv/education/" + str(new_item.pk) + "/edit/"
        data={'title':"Test No Auth Education", 'location':"Institution", 'start_date':"Test date", 'end_date':"Test end", 'brief_text':"Test Brief", 'detailed_text':"Test Detailed",}
        response = self.client.post(url, data)
        self.assertEqual(Education.objects.count(), 1)
        self.assertNotEqual(response['location'], "/cv/")
        self.assertEqual(response['location'], "/accounts/login/?next="+url)
        unedited_item = Education.objects.first()
        self.assertEqual(unedited_item.title, "Test No Auth Education 2")
        self.assertEqual(unedited_item.location, "Institution No Auth 2")
        self.assertEqual(unedited_item.detailed_text, "Test No Auth 2 Detailed")
    
    def test_delete_education_unauthenticated(self):
        item = Education()
        item.title = "Test No Auth Education 3"
        item.location = "Institution No Auth 3"
        item.start_date = "Test No Auth 03"
        item.end_date = "Test No Auth 30"
        item.brief_text = "Test No Auth 3 Brief" 
        item.detailed_text = "Test No Auth 3 Detailed" 
        item.save()
        self.assertEqual(Education.objects.count(), 1)
        new_item = Education.objects.first()
        url = "/cv/education/" + str(new_item.pk) + "/remove/"
        response = self.client.get(url)
        self.assertEqual(Education.objects.count(), 1)
        self.assertNotEqual(response['location'], "/cv/")
        self.assertEqual(response['location'], "/accounts/login/?next="+url)

    def test_new_experience_form_unauthenticated(self):
        response = self.client.get('/cv/experience/new/')
        self.assertNotEqual(response['location'], "/cv/experience/new/")
        self.assertEqual(response['location'], "/accounts/login/?next=/cv/experience/new/")
    
    def test_new_experience_post_unauthenticated(self):
        data={'title':"Test No Auth Experience", 'subtitle':"Experience Type", 'date':"Test date", 'text':"Test Detailed",}
        response = self.client.post('/cv/experience/new/', data)
        self.assertEqual(Experience.objects.count(), 0)
        self.assertEqual(response['location'], "/accounts/login/?next=/cv/experience/new/")
    
    def test_edit_experience_form_unauthenticated(self):
        item = Experience()
        item.title = "Test No Auth Experience 1"
        item.subtitle = "Experience No Auth 1 Type"
        item.date = "Test No Auth 01"
        item.text = "Test No Auth 1 Detailed" 
        item.save()
        self.assertEqual(Experience.objects.count(), 1)
        new_item = Experience.objects.first()
        url = "/cv/experience/" + str(new_item.pk) + "/edit/"
        response = self.client.get(url)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertNotEqual(response['location'], url)
        self.assertEqual(response['location'], "/accounts/login/?next="+url)

    def test_edit_experience_post_unauthenticated(self):
        item = Experience()
        item.title = "Test No Auth Experience 2"
        item.subtitle = "Experience No Auth 2 Type"
        item.date = "Test No Auth 02"
        item.text = "Test No Auth 2 Detailed" 
        item.save()
        self.assertEqual(Experience.objects.count(), 1)
        new_item = Experience.objects.first()
        url = "/cv/experience/" + str(new_item.pk) + "/edit/"
        data={'title':"Test No Auth Experience", 'subtitle':"Experience Type", 'date':"Test date", 'text':"Test Detailed",}
        response = self.client.post(url, data)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertNotEqual(response['location'], "/cv/")
        self.assertEqual(response['location'], "/accounts/login/?next="+url)
        unedited_item = Experience.objects.first()
        self.assertEqual(unedited_item.title, "Test No Auth Experience 2")
        self.assertEqual(unedited_item.subtitle, "Experience No Auth 2 Type")
        self.assertEqual(unedited_item.text, "Test No Auth 2 Detailed")
    
    def test_delete_experience_unauthenticated(self):
        item = Experience()
        item.title = "Test No Auth Experience 3"
        item.subtitle = "Experience No Auth 3 Type"
        item.date = "Test No Auth 03"
        item.text = "Test No Auth 3 Detailed" 
        item.save()
        self.assertEqual(Experience.objects.count(), 1)
        new_item = Experience.objects.first()
        url = "/cv/experience/" + str(new_item.pk) + "/remove/"
        response = self.client.get(url)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertNotEqual(response['location'], "/cv/")
        self.assertEqual(response['location'], "/accounts/login/?next="+url)