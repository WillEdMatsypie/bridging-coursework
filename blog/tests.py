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

    def setup_edit(self, data):
        self.client.post('/blog/post/new/', data)
        self.assertEqual(Post.objects.count(), 1)
        new_item = Post.objects.first()
        return "/blog/post/" + str(new_item.pk) + "/edit/"

    def test_post_edit(self):
        data={'title':"Post 15", 'subtitle':"Subtitle 15", 'text':"Text 15",}
        url = self.setup_edit(data)
        data2={'title':"Post 150", 'subtitle':"Subtitle 150", 'text':"Text 150",}
        response = self.client.post(url, data2)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(response['location'], "/blog/post/" + str(Post.objects.first().pk) + "/")
        edited_item = Post.objects.first()
        self.assertEqual(edited_item.title, "Post 150")
        self.assertEqual(edited_item.subtitle, "Subtitle 150")
        self.assertEqual(edited_item.text, "Text 150")
    
    def test_post_edit_404(self):
        data={'title':"Post 16", 'subtitle':"Subtitle 16", 'text':"Text 16",}
        url = "/blog/post/" + str(1) + "/edit/"
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Post.objects.count(), 0)
    
    def test_url_resolves_to_post_form_edit_view(self):
        data={'title':"Post 17", 'subtitle':"Subtitle 17", 'text':"Text 17",}
        url = self.setup_edit(data)
        found = resolve(url)  
        self.assertEqual(found.func, post_edit)
    
    def test_uses_post_form_edit_template(self):
        data={'title':"Post 18", 'subtitle':"Subtitle 18", 'text':"Text 18",}
        url = self.setup_edit(data)
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'post_edit.html')
    
    def test_view_post_edit_form(self):
        data={'title':"Post 19", 'subtitle':"Subtitle 19", 'text':"Text 19",}
        url= self.setup_edit(data)
        response = self.client.get(url)
        self.assertIsInstance(response.context['form'], PostForm) 
        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'name="subtitle')
        self.assertContains(response, 'name="text')
    
class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client.login(username='temporary', password='temporary')
        self.post = Post()
        self.post.title = "Base 1"
        self.post.subtitle = "Base Subtitle 1"
        self.post.text = "Base Text 1"
        self.post.author = self.user
        self.post.save()

    def tearDown(self):
        self.client.logout()
        self.user.delete()
        self.post.delete()

    def test_saving_and_retrieving_comment(self):

        first_item = Comment()
        first_item.post = self.post
        first_item.author = "Author 1"
        first_item.text = "Text 1"
        first_item.save()

        other_post = Post()
        other_post.title = "Base 2"
        other_post.subtitle = "Base Subtitle 2"
        other_post.text = "Base Text 2"
        other_post.author = self.user
        other_post.save()

        second_item = Comment()
        second_item.post = other_post
        second_item.author = "Author 2"
        second_item.text = "Text 2"
        second_item.save()

        third_item = Comment()
        third_item.post = other_post
        third_item.author = "Author 3"
        third_item.text = "Text 3"
        third_item.save()

        saved_items = Comment.objects.all()
        self.assertEqual(saved_items.count(), 3)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        third_saved_item = saved_items[2]
        self.assertEqual(first_saved_item.author, 'Author 1')
        self.assertEqual(second_saved_item.author, 'Author 2')
        self.assertEqual(third_saved_item.author, 'Author 3')
        self.assertEqual(first_saved_item.post, self.post)
        self.assertEqual(second_saved_item.post, other_post)
        self.assertEqual(third_saved_item.post, other_post)

        self.assertEqual(self.post.comments.count(), 1)
        self.assertEqual(other_post.comments.count(), 2)

        post_comments1 = self.post.comments.all()
        post_comments2 = other_post.comments.all()

        self.assertEqual(first_saved_item, post_comments1[0])
        self.assertEqual(second_saved_item, post_comments2[0])
        self.assertEqual(third_saved_item, post_comments2[1])

    def test_url_resolves_to_comment_form_view(self):
        found = resolve("/blog/post/" + str(self.post.pk) + "/comment/")  
        self.assertEqual(found.func, add_comment_to_post)
    
    def test_uses_comment_form_template(self):
        response = self.client.get("/blog/post/" + str(self.post.pk) + "/comment/")
        self.assertTemplateUsed(response, 'add_comment.html')

    def test_comment_form_returns_correct_html(self):
        request = HttpRequest()  
        request.user = self.user
        response = add_comment_to_post(request, self.post.pk)  
        html = response.content.decode('utf8')  
        self.assertTrue(html.strip().startswith('<html>'))  
        self.assertIn('<title>Zenith\'s Blog</title>', html)  
        self.assertIn('<h1>New comment</h1>', html)
        self.assertTrue(html.strip().endswith('</html>'))  
    
    def test_view_comment_form(self):
        response = self.client.get("/blog/post/" + str(self.post.pk) + "/comment/")
        self.assertIsInstance(response.context['form'], CommentForm) 
        self.assertContains(response, 'name="author"')
        self.assertContains(response, 'name="text')

    def test_can_save_POST_request_to_comment_model(self):
        data={'author':"Author 4", 'text':"Text 4",}
        response = self.client.post("/blog/post/" + str(self.post.pk) + "/comment/", data)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post.comments.count(), 1)
        new_item = Comment.objects.first()

        self.assertEqual(new_item.author, "Author 4")
        self.assertEqual(new_item.text, "Text 4")
        self.assertEqual(new_item.post, self.post)
        self.assertEqual(new_item, self.post.comments.first())
    
    def test_can_save_multiple_POST_requests_to_comment_model(self):
        data={'author':"Author 5", 'text':"Text 5",}
        response = self.client.post("/blog/post/" + str(self.post.pk) + "/comment/", data)
        data={'author':"Author 6", 'text':"Text 6",}
        response = self.client.post("/blog/post/" + str(self.post.pk) + "/comment/", data)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.post.comments.count(), 2)
        new_items = Comment.objects.all()

        new_item1 = new_items[0]
        new_item2 = new_items[1]

        self.assertEqual(new_item1.author, "Author 5")
        self.assertEqual(new_item1.text, "Text 5")
        self.assertEqual(new_item1.post, self.post)
        self.assertEqual(new_item2.author, "Author 6")
        self.assertEqual(new_item2.text, "Text 6")
        self.assertEqual(new_item2.post, self.post)
        self.assertEqual(new_item1, self.post.comments.all()[0])
        self.assertEqual(new_item2, self.post.comments.all()[1])

    def test_redirect_after_POST_submission(self):
        data={'author':"Author 7", 'text':"Text 7",}
        response = self.client.post("/blog/post/" + str(self.post.pk) + "/comment/", data)
        self.assertEqual(response.status_code, 302)
        url = "/blog/post/" + str(self.post.pk) + "/"
        self.assertEqual(response['location'], url)
    
    def test_error_response_on_incomplete_form(self):
        data={'author':"Blank Text", 'text':"",}
        response = self.client.post("/blog/post/" + str(self.post.pk) + "/comment/", data)
        self.assertEqual(Comment.objects.count(), 0) # Doesn't add to DB
        self.assertEqual(self.post.comments.count(), 0)
        self.assertTemplateUsed(response, 'add_comment.html') # Redirects to same page
    
    def test_bad_request(self):
        data={'author':"Bad Comment",}
        response = self.client.post("/blog/post/" + str(self.post.pk) + "/comment/", data)
        self.assertEqual(Comment.objects.count(), 0) #Doesn't add to database
        self.assertEqual(self.post.comments.count(), 0)
    
    def test_add_comment_404(self):
        data={'author':"Author 8", 'text':"Text 8",}
        url = "/blog/post/" + str(2) + "/comment/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Comment.objects.count(), 0)
    
    def test_approve_comment(self):
        item = Comment()
        item.post = self.post
        item.author = "Author 9"
        item.text = "Text 9"
        item.save()
        self.assertFalse(item.approved_comment)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post.comments.count(), 1)
        item.approve()
        item = Comment.objects.get(pk=item.pk)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post.comments.count(), 1)
        self.assertTrue(item.approved_comment)
        self.assertEqual(item.author, "Author 9")
        self.assertEqual(item.text, "Text 9")
        self.assertEqual(item.post, self.post)
        self.assertEqual(item, self.post.comments.first())

    def test_approve_comment_url(self):
        item = Comment()
        item.post = self.post
        item.author = "Author 10"
        item.text = "Text 10"
        item.save()
        self.assertFalse(item.approved_comment)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post.comments.count(), 1)
        url = "/blog/post/" + str(self.post.pk) + "/"
        url2 = "/blog/comment/" + str(item.pk) + "/approve/"
        response = self.client.post(url2)
        item = Comment.objects.get(pk=item.pk)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post.comments.count(), 1)
        self.assertTrue(item.approved_comment)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], url)
    
    def test_comment_approve_404(self):
        url = "/blog/comment/" + str(1) + "/approve/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Comment.objects.count(), 0)
    
    def test_comment_deletion(self):
        data={'author':"Author 11", 'text':"Text 11",}
        self.client.post("/blog/post/" + str(self.post.pk) + "/comment/", data)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post.comments.count(), 1)
        new_item = Comment.objects.first()
        new_item.delete()
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(self.post.comments.count(), 0)
    
    def test_comment_deletion_with_multiple(self):
        data={'author':"Author 12", 'text':"Text 12",}
        self.client.post("/blog/post/" + str(self.post.pk) + "/comment/", data)
        data={'author':"Author 13", 'text':"Text 13",}
        self.client.post("/blog/post/" + str(self.post.pk) + "/comment/", data)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.post.comments.count(), 2)
        new_item = Comment.objects.first()
        new_item.delete()
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post.comments.count(), 1)
        remaining_item = Comment.objects.first()
        self.assertEqual(remaining_item, self.post.comments.first())
    
    def test_comment_deletion_url(self):
        data={'author':"Author 14", 'text':"Text 14",}
        self.client.post("/blog/post/" + str(self.post.pk) + "/comment/", data)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post.comments.count(), 1)
        new_item = Comment.objects.first()
        url = "/blog/comment/" + str(new_item.pk) + "/remove/"
        response = self.client.get(url)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(self.post.comments.count(), 0)
        self.assertEqual(response['location'], "/blog/post/" + str(self.post.pk) + "/")

    def test_comment_deletion_url_with_multiple(self):
        data={'author':"Author 15", 'text':"Text 15",}
        self.client.post("/blog/post/" + str(self.post.pk) + "/comment/", data)
        data={'author':"Author 16", 'text':"Text 16",}
        self.client.post("/blog/post/" + str(self.post.pk) + "/comment/", data)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(self.post.comments.count(), 2)
        new_item = Comment.objects.first()
        url = "/blog/comment/" + str(new_item.pk) + "/remove/"
        response = self.client.get(url)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.post.comments.count(), 1)
        self.assertEqual(response['location'], "/blog/post/" + str(self.post.pk) + "/")
        remaining_item = Comment.objects.first()
        self.assertEqual(remaining_item, self.post.comments.first())
    
    def test_comment_deletion_404(self):
        url = "/blog/comment/" + str(1) + "/remove/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Comment.objects.count(), 0)
    
    def test_cascade_deletion(self):
        other_post = Post()
        other_post.title = "Base 3"
        other_post.subtitle = "Base Subtitle 3"
        other_post.text = "Base Text 3"
        other_post.author = self.user
        other_post.save()

        data={'author':"Author 17", 'text':"Text 17",}
        self.client.post("/blog/post/" + str(other_post.pk) + "/comment/", data)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(other_post.comments.count(), 1)
        other_post.delete()
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)
    
    def test_cascade_deletion_url(self):
        other_post = Post()
        other_post.title = "Base 4"
        other_post.subtitle = "Base Subtitle 4"
        other_post.text = "Base Text 4"
        other_post.author = self.user
        other_post.save()

        data={'author':"Author 18", 'text':"Text 18",}
        self.client.post("/blog/post/" + str(other_post.pk) + "/comment/", data)
        data={'author':"Author 19", 'text':"Text 19",}
        self.client.post("/blog/post/" + str(other_post.pk) + "/comment/", data)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(other_post.comments.count(), 2)
        url = "/blog/post/" + str(other_post.pk) + "/remove/"
        response = self.client.get(url)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Comment.objects.count(), 0)

