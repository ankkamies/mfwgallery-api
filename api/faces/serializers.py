from django.forms import widgets
from django.contrib.auth.models import User

from rest_framework import serializers
from faces.models import Face, Comment

class UserSerializer(serializers.HyperlinkedModelSerializer):
    faces = serializers.HyperlinkedIdentityField(many=True, view_name='face-detail', read_only=True)
    comments = serializers.HyperlinkedIdentityField(many=True, view_name='face-comment-detail')

    class Meta:
        model = User
        fields = ('id', 'username', 'faces', 'comments')

class FaceSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    comments = serializers.HyperlinkedIdentityField(many=True, view_name='face-comment-detail')

    class Meta:
        model = Face
        fields = ('user', 'created', 'description', 'image', 'thumbnail', 'comments', 'tags')

class CommentSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ('user', 'face', 'text', 'created')

