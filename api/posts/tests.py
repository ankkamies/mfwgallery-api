from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework import status
from rest_framework.test import APITestCase

from rest_framework.test import APIRequestFactory

class MFWGalleryTests(APITestCase):
    def _create_user(self):
        user = User.objects.create_user(username='testi', email='kissa@kala.fi', password='testi')
        user.save()
        return user

    # Create user and log in
    def setUp(self):
        self.user = self._create_user()
        self.logged_in = self.client.login(username=self.user.username, password='testi')

    def test_upload_valid_image(self):
        """
        Tests posting a valid image url
        """    
        url = reverse('mfwgallery:post')
        image = SimpleUploadedFile("image.jpg", "file_content", content_type="image/jpeg")
        data = {"description": "This is a valid image", "image": image}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Not working because auto_now_add
        # self.assertEqual(response.data, {"nick": "tester", "description": "This is a valid image", "url": "http://i.imgur.com/YnFMv0i.png", "image": "images/YnFMv0i.png", "thumbnail": "images/thumbs/YnFMv0i_uu.png"})
