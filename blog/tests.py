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
        self.assertNotIn('<a class="btn btn-outline-light center" id="new-post" href="/blog/post/new/">New Post</span></a>', html)
    
    def test_new_post_button_auth(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/blog/') 
        html = response.content.decode('utf8')  
        self.assertIn('<a class="btn btn-outline-light center" id="new-post" href="/blog/post/new/">New Post</span></a>', html)
        self.client.logout()


class DraftListTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def tearDown(self):
        self.user.delete()
    
    def test_draft_url_resolves_to_draft_list_view(self):
        found = resolve('/blog/drafts/')  
        self.assertEqual(found.func, post_draft_list)
    
    def test_uses_draft_list_template(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/blog/drafts/')
        self.assertTemplateUsed(response, 'post_draft_list.html')
        self.client.logout()
    
    def test_draft_list_returns_correct_html(self):
        request = HttpRequest()  
        request.user = self.user
        response = post_draft_list(request)  
        html = response.content.decode('utf8')  
        self.assertTrue(html.strip().startswith('<html>'))  
        self.assertIn('<title>Zenith\'s Blog</title>', html)  
        self.assertTrue(html.strip().endswith('</html>'))  
    
    def test_new_post_button_no_auth(self):
        response = self.client.get('/blog/drafts/') 
        html = response.content.decode('utf8')  
        self.assertNotIn('<a class="btn btn-outline-light center" id="new-post" href="/blog/post/new/">New Post</span></a>', html)
    
    def test_new_post_button_auth(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/blog/drafts/') 
        html = response.content.decode('utf8')  
        self.assertIn('<a class="btn btn-outline-light center" id="new-post" href="/blog/post/new/">New Post</span></a>', html)
        self.client.logout()

class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')

    def tearDown(self):
        self.client.logout()
        self.user.delete()

    def test_saving_and_retrieving_post(self):
        first_item = Post()
        first_item.title = "Post 1"
        first_item.subtitle = "Subtitle 1"
        first_item.text = "Text 1"
        first_item.author = self.user
        first_item.save()


        second_item = Post()
        second_item.title = "Post 2"
        second_item.subtitle = "Subtitle 2"
        second_item.text = "Text 2"
        second_item.author = self.user
        second_item.save()
        
        saved_items = Post.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.title, 'Post 1')
        self.assertEqual(second_saved_item.title, 'Post 2')

    def test_url_resolves_to_post_form_view(self):
        found = resolve('/blog/post/new/')  
        self.assertEqual(found.func, post_new)
    
    def test_uses_post_form_template(self):
        response = self.client.get('/blog/post/new/')
        self.assertTemplateUsed(response, 'post_edit.html')

    def test_post_form_returns_correct_html(self):
        request = HttpRequest()  
        request.user = self.user
        response = post_new(request)  
        html = response.content.decode('utf8')  
        self.assertTrue(html.strip().startswith('<html>'))  
        self.assertIn('<title>Zenith\'s Blog</title>', html)  
        self.assertIn('<h2>New post</h2>', html)
        self.assertTrue(html.strip().endswith('</html>'))  
    
    def test_view_post_form(self):
        response = self.client.get('/blog/post/new/')
        self.assertIsInstance(response.context['form'], PostForm) 
        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'name="subtitle')
        self.assertContains(response, 'name="text')

    def test_can_save_POST_request_to_post_model(self):
        data={'title':"Post 3", 'subtitle':"Subtitle 3", 'text':"Text 3",}
        response = self.client.post('/blog/post/new/', data)
        self.assertEqual(Post.objects.count(), 1)
        new_item = Post.objects.first()
        self.assertEqual(new_item.title, "Post 3")
        self.assertEqual(new_item.subtitle, "Subtitle 3")
        self.assertEqual(new_item.text, "Text 3")

    def test_redirect_after_POST_submission(self):
        data={'title':"Post 4", 'subtitle':"Subtitle 4", 'text':"Text 4",}
        response = self.client.post('/blog/post/new/', data)
        self.assertEqual(response.status_code, 302)
        url = "/blog/post/" + str(Post.objects.first().pk) + "/"
        self.assertEqual(response['location'], url)
    
    def test_error_response_on_incomplete_form(self):
        data={'title':"Post Blank Text & Subtitle", 'subtitle':"", 'text':"",}
        response = self.client.post('/blog/post/new/', data)
        self.assertEqual(Post.objects.count(), 0) # Doesn't add to DB
        self.assertTemplateUsed(response, 'post_edit.html') # Redirects to same page
    
    def test_bad_request(self):
        data={'title':"Bad Post",}
        response = self.client.post('/blog/post/new/', data)
        self.assertEqual(Post.objects.count(), 0) #Doesn't add to database

    def test_post_url_resolves_to_detail_view(self):
        data={'title':"Post 5", 'subtitle':"Subtitle 5", 'text':"Text 5",}
        response = self.client.post('/blog/post/new/', data)
        url = "/blog/post/" + str(Post.objects.first().pk) + "/"
        found = resolve(url)  
        self.assertEqual(found.func, post_detail)
    
    def test_uses_post_detail_template(self):
        data={'title':"Post 6", 'subtitle':"Subtitle 6", 'text':"Text 6",}
        response = self.client.post('/blog/post/new/', data)
        url = "/blog/post/" + str(Post.objects.first().pk) + "/"
        response2 = self.client.get(url)
        self.assertTemplateUsed(response2, 'post_detail.html')
    
    def test_post_detail_returns_correct_html(self):
        data={'title':"Post 7", 'subtitle':"Subtitle 7", 'text':"Text 7",}
        response = self.client.post('/blog/post/new/', data)
        request = HttpRequest()  
        request.user = self.user
        response2 = post_detail(request, Post.objects.first().pk)  
        html = response2.content.decode('utf8')  
        self.assertTrue(html.strip().startswith('<html>'))  
        self.assertIn('<title>Zenith\'s Blog</title>', html)  
        self.assertIn('<h1 style="text-align: center;">Post 7</h1>', html)
        self.assertTrue(html.strip().endswith('</html>'))  

    def test_post_detail_404(self):
        data={'title':"Post 10", 'subtitle':"Subtitle 10", 'text':"Text 10",}
        url = "/blog/post/" + str(1) + "/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_publish_post(self):
        item = Post()
        item.title = "Post 8"
        item.subtitle = "Subtitle 8"
        item.text = "Text 8"
        item.author = self.user
        item.save()
        self.assertEqual(item.published_date, None)
        self.assertEqual(Post.objects.count(), 1)
        item.publish()
        item = Post.objects.get(pk=item.pk)
        self.assertEqual(Post.objects.count(), 1)
        self.assertNotEqual(item.published_date, None)
        self.assertEqual(item.title, "Post 8")
        self.assertEqual(item.subtitle, "Subtitle 8")
        self.assertEqual(item.text, "Text 8")

    def test_publish_post_url(self):
        item = Post()
        item.title = "Post 9"
        item.subtitle = "Subtitle 9"
        item.text = "Text 9"
        item.author = self.user
        item.save()
        self.assertEqual(item.published_date, None)
        self.assertEqual(Post.objects.count(), 1)
        url = "/blog/post/" + str(item.pk) + "/"
        url2 = url + "publish/"
        response = self.client.post(url2)
        item = Post.objects.get(pk=item.pk)
        self.assertEqual(Post.objects.count(), 1)
        self.assertNotEqual(item.published_date, None)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], url)
    
    def test_post_publish_404(self):
        data={'title':"Post 11", 'subtitle':"Subtitle 11", 'text':"Text 11",}
        url = "/blog/post/" + str(1) + "/publish/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Post.objects.count(), 0)
        
    def test_post_deletion(self):
        data={'title':"Post 12", 'subtitle':"Subtitle 12", 'text':"Text 12",}
        self.client.post('/blog/post/new/', data)
        self.assertEqual(Post.objects.count(), 1)
        new_item = Post.objects.first()
        new_item.delete()
        self.assertEqual(Post.objects.count(), 0)
    
    def test_post_deletion_url(self):
        data={'title':"Post 13", 'subtitle':"Subtitle 13", 'text':"Text 13",}
        self.client.post('/blog/post/new/', data)
        self.assertEqual(Post.objects.count(), 1)
        new_item = Post.objects.first()
        url = "/blog/post/" + str(new_item.pk) + "/remove/"
        response = self.client.get(url)
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(response['location'], "/blog/")
    
    def test_post_deletion_404(self):
        data={'title':"Post 14", 'subtitle':"Subtitle 14", 'text':"Text 14",}
        url = "/blog/post/" + str(1) + "/remove/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Post.objects.count(), 0)

    # def setup_edit(self, data):
    #     self.client.post('/cv/skill/new/', data)
    #     self.assertEqual(Skill.objects.count(), 1)
    #     new_item = Skill.objects.first()
    #     return "/cv/skill/" + str(new_item.pk) + "/edit/"

    # def test_skill_edit(self):
    #     data={'title':"Skill 8", 'skill_type':"other",}
    #     url = self.setup_edit(data)
    #     data2={'title':"Skill 80", 'skill_type':"technical",}
    #     response = self.client.post(url, data2)
    #     self.assertEqual(Skill.objects.count(), 1)
    #     self.assertEqual(response['location'], "/cv/")
    #     edited_item = Skill.objects.first()
    #     self.assertEqual(edited_item.title, "Skill 80")
    #     self.assertEqual(edited_item.skill_type, "technical")
    
    # def test_skill_edit_404(self):
    #     data={'title':"Skill 9", 'skill_type':"other",}
    #     url = "/cv/skill/" + str(1) + "/edit/"
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(Skill.objects.count(), 0)
    
    # def test_url_resolves_to_skill_form_edit_view(self):
    #     data={'title':"Skill 10", 'skill_type':"technical",}
    #     url = self.setup_edit(data)
    #     found = resolve(url)  
    #     self.assertEqual(found.func, skill_edit)
    
    # def test_uses_skill_form_edit_template(self):
    #     data={'title':"Skill 11", 'skill_type':"technical",}
    #     url = self.setup_edit(data)
    #     response = self.client.get(url)
    #     self.assertTemplateUsed(response, 'cv/skill_edit.html')
    
    # def test_view_skill_edit_form(self):
    #     data={'title':"Skill 12", 'skill_type':"technical",}
    #     url = self.setup_edit(data)
    #     response = self.client.get(url)
    #     self.assertIsInstance(response.context['form'], SkillForm) 
    #     self.assertContains(response, 'name="title"')
    #     self.assertContains(response, 'name="skill_type')
