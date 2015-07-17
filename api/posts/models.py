import os
import hashlib
import time
import requests

from sys import getsizeof
from PIL import Image
from io import BytesIO

from django.conf import settings
from django.core.files.images import ImageFile
from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile

from django.db import models
from django.utils import timezone

class Comment(models.Model):
    user = models.ForeignKey('auth.User', related_name='comments')
    post = models.ForeignKey('Post', related_name='comments')
    text = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<%n> %t' & (self.user.username, self.text)

class Tag(models.Model):
    text = models.CharField(max_length=60, primary_key=True)

    def __str__(self):
        return self.text;

class ImageModel(models.Model):
    file = models.ImageField(upload_to='images', null = True)
    thumbnail = models.ImageField(upload_to='images/thumbs', null = True)
    url = models.CharField(max_length=300, null = True)

    def get_image(self):
        THUMB_SIZE = (256,256)         
        FILE_EXTENSION = os.path.splitext(self.url)[1]
        print(FILE_EXTENSION)
        # Generate new filename
        hash = hashlib.sha1(str(time.time()).encode())

        self.file.name = hash.hexdigest()[:10] + '.' + FILE_EXTENSION

        filename = hash.hexdigest()[:10] + FILE_EXTENSION
        path = settings.MEDIA_ROOT + 'tmp' + FILE_EXTENSION
        # Retrieve image and save it to FileField
        r = requests.get(self.url, stream=True)
        if r.status_code == 200:
            print('Downloading image...')
            with open(path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)

        if FILE_EXTENSION == '.jpg' or FILE_EXTENSION == '.jpeg':
            PIL_TYPE = 'jpeg'
            DJANGO_TYPE = 'image/jpeg'
        elif FILE_EXTENSION == '.png':
            PIL_TYPE = 'png'
            DJANGO_TYPE = 'image/png'
        elif FILE_EXTENSION == '.gif':
            PIL_TYPE = 'gif'
            DJANGO_TYPE = 'image/gif'

        image = Image.open(path)

        temp_handle = BytesIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        mem_file = InMemoryUploadedFile(temp_handle, image, filename, DJANGO_TYPE, getsizeof(temp_handle), None)
        self.file.save('%s%s'%((os.path.splitext(mem_file.name))[0], FILE_EXTENSION), mem_file, save=False)
        
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

        temp_handle = BytesIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        mem_file = InMemoryUploadedFile(temp_handle, image, filename, DJANGO_TYPE, getsizeof(temp_handle), None)
        self.thumbnail.save('%s_uu%s'%((os.path.splitext(mem_file.name))[0], FILE_EXTENSION), mem_file, save=False)

    def create_thumbnail(self):
        THUMB_SIZE = (256,256)
        DJANGO_TYPE = self.file.file.content_type

        if DJANGO_TYPE == 'image/jpeg':
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
        elif DJANGO_TYPE == 'image/png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
        elif DJANGO_TYPE == 'image/gif':
            PIL_TYPE = 'gif'
            FILE_EXTENSION = 'gif'

        image = Image.open(BytesIO(self.file.read()))

        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

        temp_handle = BytesIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        # Generate new filename
        hash = hashlib.sha1(str(time.time()).encode())

        self.file.name = hash.hexdigest()[:10] + '.' + FILE_EXTENSION

        # Save image to a SimpleUploadFile temporarily
        mem_file = InMemoryUploadedFile(temp_handle, image, os.path.split(self.file.name)[-1], DJANGO_TYPE, getsizeof(temp_handle), None)
        self.thumbnail.save('%s_uu.%s'%((os.path.splitext(mem_file.name))[0], FILE_EXTENSION), mem_file, save=False)

    def save(self, *args, **kwargs):
        if (self.url != None):
            self.get_image()
        elif (self.file != None):
            self.create_thumbnail()
        else:
            return
        super(ImageModel, self).save(*args, **kwargs)

class Post(models.Model):
    user = models.ForeignKey('auth.User', related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    image = models.OneToOneField('ImageModel', related_name='post')
    tags = models.ManyToManyField('Tag', related_name='posts')
