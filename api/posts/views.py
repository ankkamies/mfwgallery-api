from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework import generics

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.models import Post, Comment, Tag, ImageModel
from posts.serializers import UserSerializer, PostSerializer, NewPostSerializer, CommentSerializer, TagSerializer, ImageSerializer, NewUserSerializer

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

    def create(self, request):
        serializer = NewPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
        queryset = self.queryset.get(pk=pk, post=post_pk)
        serializer = CommentSerializer(queryset)
        return Response(serializer.data)

    def perform_create(self, serializer, post):
        serializer.save(user=self.request.user, post=post)

