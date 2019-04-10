from rest_framework.test import APITestCase
from rest_framework import status
from posts.models import Post
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as api_reverse

from rest_framework_jwt.settings import api_settings
payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER


User = get_user_model()


class BlogPostAPITestCase(APITestCase):

    def setUp(self):
        user_obj = User.objects.create(username='testcfeuser', email='test@test.com')
        user_obj.set_password('somerandopassword')
        user_obj.save()
        blog_post = Post.objects.create(user=user_obj, title='New Title', content='some_random_content whey')

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

    def test_single_post(self):
        post_count = Post.objects.count()
        self.assertEqual(post_count, 1)

    def test_get_list(self):
        data = {}
        url = api_reverse('api-postings:post-listcreate')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    def test_post_item(self):
        data = {'title': 'some rando title', 'content': 'some more content'}
        url = api_reverse('api-postings:post-listcreate') 
        response = self.client.post(url, data, format='json')
        # should be 401 because unauthourized users cannot post blog
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item(self):
        """"Tests that HTTP method is disallowed if we try to POST to an existing blog_post"""

        blog_post = Post.objects.first()
        url = blog_post.get_api_url()
        data = {'title': 'some rando title', 'content': 'some more content'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # test that we cannot make a PUT if we haven't logged in
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item_for_authenticated_user(self):
        """"Tests that HTTP method is disallowed if we try to POST to an existing blog_post"""

        blog_post = Post.objects.first()
        url = blog_post.get_api_url()
        data = {'title': 'some rando title', 'content': 'some more content'}
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)

        # test that we cannot make a PUT if we haven't logged in
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login(self):
        data = {'username': 'testcfeuser', 'password': 'somerandopassword'}
        url = api_reverse('api-login')
        rsp = self.client.post(url, data)
        print(rsp.data)
        self.assertEqual(rsp.status_code, status.HTTP_200_OK)
