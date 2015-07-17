from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework import generics
from rest_framework import filters

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post, Comment, Tag, ImageModel
from posts.serializers import UserSerializer, PostSerializer, NewPostSerializer, UpdatePostSerializer, CommentSerializer, TagSerializer, ImageSerializer, UrlImageSerializer, NewUserSerializer

from mfwgallery.permissions import IsAuthenticatedOrCreate

class LoginView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        return Response(self.serializer_class(request.user).data)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = NewUserSerializer
    permission_classes = (AllowAny,)

class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer

class UrlImagePostView(generics.ListCreateAPIView):
    queryset = ImageModel.objects.all()
    serializer_class = UrlImageSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrCreate,)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, username=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('created',)

    def create(self, request):
        # Handle adding tags
        tags = []
        tag_queryset = Tag.objects.all()
        
        # Check if tags already exist
        for tag in request.data['tags']:
            if not tag_queryset.filter(text=tag).exists():
                # Keep tags that do not exist
                tags.append({'text':tag})

        # Serialize and save tags that do not exist
        tag_serializer = TagSerializer(data=tags, many=True)
        tag_serializer.is_valid(raise_exception=True)
        tag_serializer.save()

        # Save post
        serializer = NewPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, pk=None, partial=False):
        # Handle adding tags
        tags = []
        tag_queryset = Tag.objects.all()
        
        # Check if tags already exist
        for tag in request.data['tags']:
            if not tag_queryset.filter(text=tag).exists():
                # Keep tags that do not exist
                tags.append({'text':tag})

        # Serialize and save tags that do not exist
        if tags:
            print(tags)
            tag_serializer = TagSerializer(data=tags, many=True)
            tag_serializer.is_valid(raise_exception=True)
            tag_serializer.save()

        # Update post
        instance = self.queryset.get(pk=pk)
        serializer = UpdatePostSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserPostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # GET /users/{username}/posts/
    def list(self, request, user_pk=None):
        user = User.objects.get(username=user_pk)
        queryset = self.queryset.filter(user=user)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    # GET /users/{username}/posts/{post_id}
    def retrieve(self, request, pk=None, user_pk=None):
        user = User.objects.get(username=user_pk)
        queryset = self.queryset.get(pk=pk, user=user)
        serializer = PostSerializer(queryset)
        return Response(serializer.data)

class PostTagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, post_pk=None):
        queryset = self.queryset.filter(post=post_pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, post_pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.perform_create(serializer, post)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, pk=None, post_pk=None):
        instance = self.queryset.get(pk=pk, post=post_pk)
        serializer = CommentSerializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer, post):
        serializer.save(user=self.request.user, post=post)

