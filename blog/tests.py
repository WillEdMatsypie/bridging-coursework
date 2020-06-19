from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.contrib.auth.models import User

from blog.views import post_list, post_detail, post_new, post_edit, post_draft_list, post_publish, post_remove, add_comment_to_post, comment_approve, comment_remove
from blog.models import Post, Comment  
from .forms import PostForm, CommentForm

class PostListTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def tearDown(self):
        self.user.delete()
    
    def test_root_url_resolves_to_post_list_view(self):
        found = resolve('/blog/')  
        self.assertEqual(found.func, post_list)
    
    def test_uses_post_list_template(self):
        response = self.client.get('/blog/')
        self.assertTemplateUsed(response, 'post_list.html')
    
    def test_post_list_returns_correct_html(self):
        request = HttpRequest()  
        response = post_list(request)  
        html = response.content.decode('utf8')  
        self.assertTrue(html.strip().startswith('<html>'))  
        self.assertIn('<title>Zenith\'s Blog</title>', html)  
        self.assertTrue(html.strip().endswith('</html>'))  
    
    def test_new_post_button_no_auth(self):
        response = self.client.get('/blog/') 
        html = response.content.decode('utf8')  
        self.assertNotIn('<a class="btn btn-outline-light center" href="/blog/post/new/">New Post</span></a>', html)
    
    def test_new_post_button_auth(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/blog/') 
        html = response.content.decode('utf8')  
        self.assertIn('<a class="btn btn-outline-light center" href="/blog/post/new/">New Post</span></a>', html)
        self.client.logout()

# class SkillModelTest(TestCase):

#     def setUp(self):
#         self.user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
#         self.client.login(username='temporary', password='temporary')

#     def tearDown(self):
#         self.client.logout()
#         self.user.delete()

#     def test_saving_and_retrieving_skill(self):
#         first_item = Skill()
#         first_item.title = "Skill 1"
#         first_item.skill_type = "technical"
#         first_item.save()


#         second_item = Skill()
#         second_item.title = "Skill 2"
#         second_item.skill_type = "other"
#         second_item.save()
        
#         saved_items = Skill.objects.all()
#         self.assertEqual(saved_items.count(), 2)

#         first_saved_item = saved_items[0]
#         second_saved_item = saved_items[1]
#         self.assertEqual(first_saved_item.title, 'Skill 1')
#         self.assertEqual(second_saved_item.title, 'Skill 2')

#     def test_url_resolves_to_skill_form_view(self):
#         found = resolve('/cv/skill/new/')  
#         self.assertEqual(found.func, skill_new)
    
#     def test_uses_skill_form_template(self):
#         response = self.client.get('/cv/skill/new/')
#         self.assertTemplateUsed(response, 'cv/skill_edit.html')

#     def test_skill_form_returns_correct_html(self):
#         request = HttpRequest()  
#         request.user = self.user
#         response = skill_new(request)  
#         html = response.content.decode('utf8')  
#         self.assertTrue(html.strip().startswith('<html>'))  
#         self.assertIn('<title>Zenith\'s Blog</title>', html)  
#         self.assertIn('<h2>New Skill</h2>', html)
#         self.assertTrue(html.strip().endswith('</html>'))  
    
#     def test_view_skill_form(self):
#         response = self.client.get('/cv/skill/new/')
#         self.assertIsInstance(response.context['form'], SkillForm) 
#         self.assertContains(response, 'name="title"')
#         self.assertContains(response, 'name="skill_type')

#     def test_can_save_POST_request_to_skill_model(self):
#         data={'title':"Skill 3", 'skill_type':"technical",}
#         response = self.client.post('/cv/skill/new/', data)
#         self.assertEqual(Skill.objects.count(), 1)
#         new_item = Skill.objects.first()
#         self.assertEqual(new_item.title, "Skill 3")
#         self.assertEqual(new_item.skill_type, "technical")
    
#     def test_redirect_after_POST_submission(self):
#         data={'title':"Skill 4", 'skill_type':"other",}
#         response = self.client.post('/cv/skill/new/', data)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(response['location'], "/cv/")
    
#     def test_error_response_on_incomplete_form(self):
#         data={'title':"", 'skill_type':"",}
#         response = self.client.post('/cv/skill/new/', data)
#         self.assertEqual(Skill.objects.count(), 0) # Doesn't add to DB
#         self.assertTemplateUsed(response, 'cv/skill_edit.html') # Redirects to same page
    
#     def test_bad_request(self):
#         data={'title':"Oops",}
#         response = self.client.post('/cv/skill/new/', data)
#         self.assertEqual(Skill.objects.count(), 0) #Doesn't add to database
        
#     def test_skill_deletion(self):
#         data={'title':"Skill 6", 'skill_type':"technical",}
#         self.client.post('/cv/skill/new/', data)
#         self.assertEqual(Skill.objects.count(), 1)
#         new_item = Skill.objects.first()
#         new_item.delete()
#         self.assertEqual(Skill.objects.count(), 0)
    
#     def test_skill_deletion_url(self):
#         data={'title':"Skill 7", 'skill_type':"other",}
#         self.client.post('/cv/skill/new/', data)
#         self.assertEqual(Skill.objects.count(), 1)
#         new_item = Skill.objects.first()
#         url = "/cv/skill/" + str(new_item.pk) + "/remove/"
#         response = self.client.get(url)
#         self.assertEqual(Skill.objects.count(), 0)
#         self.assertEqual(response['location'], "/cv/")

#     def setup_edit(self, data):
#         self.client.post('/cv/skill/new/', data)
#         self.assertEqual(Skill.objects.count(), 1)
#         new_item = Skill.objects.first()
#         return "/cv/skill/" + str(new_item.pk) + "/edit/"

#     def test_skill_edit(self):
#         data={'title':"Skill 8", 'skill_type':"other",}
#         url = self.setup_edit(data)
#         data2={'title':"Skill 80", 'skill_type':"technical",}
#         response = self.client.post(url, data2)
#         self.assertEqual(Skill.objects.count(), 1)
#         self.assertEqual(response['location'], "/cv/")
#         edited_item = Skill.objects.first()
#         self.assertEqual(edited_item.title, "Skill 80")
#         self.assertEqual(edited_item.skill_type, "technical")
    
#     def test_skill_edit_404(self):
#         data={'title':"Skill 9", 'skill_type':"other",}
#         url = "/cv/skill/" + str(1) + "/edit/"
#         response = self.client.post(url, data)
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(Skill.objects.count(), 0)
    
#     def test_url_resolves_to_skill_form_edit_view(self):
#         data={'title':"Skill 10", 'skill_type':"technical",}
#         url = self.setup_edit(data)
#         found = resolve(url)  
#         self.assertEqual(found.func, skill_edit)
    
#     def test_uses_skill_form_edit_template(self):
#         data={'title':"Skill 11", 'skill_type':"technical",}
#         url = self.setup_edit(data)
#         response = self.client.get(url)
#         self.assertTemplateUsed(response, 'cv/skill_edit.html')
    
#     def test_view_skill_edit_form(self):
#         data={'title':"Skill 12", 'skill_type':"technical",}
#         url = self.setup_edit(data)
#         response = self.client.get(url)
#         self.assertIsInstance(response.context['form'], SkillForm) 
#         self.assertContains(response, 'name="title"')
#         self.assertContains(response, 'name="skill_type')
