from rest_framework import serializers
from posts.models import Post, Comment, Tag, ImageModel
from django.contrib.auth.models import User

class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'username', 'first_name', 'last_name', 'email')
        write_only_fields = ('password',)

    def create(self, attrs):
        user = User.objects.create_user(attrs.get('username'), attrs.get('email'), attrs.get('password'))
        user.first_name = attrs.get('first_name')
        user.last_name = attrs.get('last_name')
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())
    comments = serializers.PrimaryKeyRelatedField(many=True, queryset=Comment.objects.all())

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'posts', 'comments')
        write_only_fields = ('password',)

    def update(self, instance, attrs):
        instance.first_name = attrs.get('first_name', instance.first_name)
        instance.last_name = attrs.get('last_name', instance.last_name)
        instance.email = attrs.get('email', instance.email)
        instance.save()
        return instance

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = ('id', 'file', 'thumbnail', 'post')
        read_only_fields = ('thumbnail', 'post',)

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ('user', 'text', 'created')

class NewPostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id') 
    tags = serializers.SlugRelatedField(
            slug_field='text',
            queryset=Tag.objects.all(),
            many=True)

    class Meta:
        model = Post
        fields = ('user', 'created', 'description', 'image', 'tags')

class PostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    image = ImageSerializer()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('user', 'username', 'id', 'created', 'description', 'image', 'comments', 'tags')

class TagSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ('text', 'posts')
