from rest_framework import serializers
from faces.models import Face, Comment, Tag, ImageModel
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'username', 'first_name', 'last_name', 'email')
        write_only_fields = ('password',)

    def create(self, attrs):
        user = User.objects.create_user(attrs.get('username'), attrs.get('email'), attrs.get('password'))
        user.first_name = attrs.get('first_name')
        user.last_name = attrs.get('last_name')
        return user

    def update(self, instance, attrs):
        instance.first_name = attrs.get('first_name', instance.first_name)
        instance.last_name = attrs.get('last_name', instance.last_name)
        instance.email = attrs.get('email', instance.email)
        return instance

class UserGetSerializer(serializers.ModelSerializer):
    faces = serializers.PrimaryKeyRelatedField(many=True, queryset=Face.objects.all())
    comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'faces', 'comments')

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('text',)

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ('id','file', 'thumbnail', 'face')
        read_only_fields = ('thumbnail', 'face')

class FaceSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    image = serializers.PrimaryKeyRelatedField(queryset=ImageModel.objects.all())

    class Meta:
        model = Face
        fields = ('user', 'username', 'created', 'description', 'image', 'tags')

class TagGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('text', 'faces')

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ('user', 'face', 'text', 'created')
        read_only_fields = ('face',)

class FaceGetSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    comments = CommentSerializer(many=True, read_only=True)
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Face
        fields = ('user', 'username', 'id', 'created', 'description', 'image', 'comments', 'tags')
        read_only_fields = ('thumbnail', 'comments')
        depth = 1

