from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from django.views.decorators.csrf import ensure_csrf_cookie

from faces.models import Face, Comment, Tag
from faces.serializers import UserSerializer, UserGetSerializer, FaceSerializer, FaceGetSerializer, CommentSerializer, TagSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        serializer = UserGetSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.queryset.get(pk=pk)
        serializer = UserGetSerializer(queryset)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()

class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Face.objects.all()
    serializer_class = FaceSerializer

    def list(self, request):
        serializer = FaceGetSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.queryset.get(pk=pk)
        serializer = FaceGetSerializer(queryset)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, face_pk=None):
        queryset = self.queryset.filter(face=face_pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, face_pk):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            face = Face.objects.get(pk=face_pk)
        except Face.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.perform_create(serializer, face)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, pk=None, face_pk=None):
        queryset = self.queryset.get(pk=pk, face=face_pk)
        serializer = CommentSerializer(queryset)
        return Response(serializer.data)

    def perform_create(self, serializer, face):
        serializer.save(user=self.request.user, face=face)

