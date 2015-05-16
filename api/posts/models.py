import os
import hashlib
import time

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
    file = models.ImageField(upload_to='images')
    thumbnail = models.ImageField(upload_to='images/thumbs', null = True)

    def create_thumbnail(self):
        if not self.file:
            return

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
        self.create_thumbnail()
        super(ImageModel, self).save(*args, **kwargs)

class Post(models.Model):
    user = models.ForeignKey('auth.User', related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    image = models.OneToOneField('ImageModel', related_name='post')
    tags = models.ManyToManyField('Tag', related_name='posts')
