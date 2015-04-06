from django.forms import widgets
from django.contrib.auth.models import User, UserManager

from rest_framework import serializers
from faces.models import Face, Comment

class UserSerializer(serializers.ModelSerializer):
    faces = serializers.PrimaryKeyRelatedField(many=True, queryset=Face.objects.all())
    comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())

    class Meta:
        model = User
        fields = ('password', 'username', 'first_name', 'last_name', 'email', 'faces', 'comments')
        write_only_fields = ('password',)

    def create(self, attrs):
        user = UserManager.create_user(attrs.get('username'), attrs.get('email'), attrs.get('password'))
        user.first_name = attrs.get('first_name')
        user.last_name = attrs.get('last_name')
        return user

    def update(self, instance, attrs):
        instance.first_name = attrs.get('first_name', instance.first_name)
        instance.last_name = attrs.get('last_name', instance.last_name)
        instance.email = attrs.get('email', instance.email)
        return instance

class FaceSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Face.objects.all())

    class Meta:
        model = Face
        fields = ('user', 'created', 'description', 'image', 'thumbnail', 'comments', 'tags')

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ('user', 'face', 'text', 'created')

