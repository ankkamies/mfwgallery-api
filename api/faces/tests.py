from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APITestCase

class MFWGalleryTests(APITestCase):
    def _create_user(self):
        user = User.objects.create_user(username='testi', email='kissa@kala.fi', password='testi')
        user.save()
        return user

    # Create user and log in
    def setUp(self):
        self.user = self._create_user()
        self.logged_in = self.client.login(username=self.user.username, password='testi')

    def test_post_valid_image(self):
        """
        Tests posting a valid image url
        """    
        url = reverse('mfwgallery:post')
        data = {"nick": "tester", "description": "This is a valid image", "url": "http://fi2.eu.apcdn.com/full/123736.jpeg"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Not working because auto_now_add
        # self.assertEqual(response.data, {"nick": "tester", "description": "This is a valid image", "url": "http://i.imgur.com/YnFMv0i.png", "image": "images/YnFMv0i.png", "thumbnail": "images/thumbs/YnFMv0i_uu.png"})

    def test_post_invalid_image(self):
        """
        Tests posting a valid image url
        """
        url = reverse('mfwgallery:post')
        data = {"nick": "tester", "description": "This is not an image", "url": "http://www.cs.tut.fi/~peliohj/harjoitustyo.html"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {})

    def test_post_not_logged_in(self):
        """
        Tests posting when not logged in
        """
        self.client.logout()
        url = reverse('mfwgallery:post')
        data = {"nick": "tester", "description": "This is a valid image", "url": "http://i.imgur.com/YnFMv0i.png"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_upload_valid_image(self):
        """
        Tests posting a valid image url
        """    
        url = reverse('mfwgallery:post')
        image = SimpleUploadedFile("image.jpg", "file_content", content_type="image/jpeg")
        data = {"nick": "tester", "description": "This is a valid image", "image": image}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Not working because auto_now_add
        # self.assertEqual(response.data, {"nick": "tester", "description": "This is a valid image", "url": "http://i.imgur.com/YnFMv0i.png", "image": "images/YnFMv0i.png", "thumbnail": "images/thumbs/YnFMv0i_uu.png"})
