from django.contrib.auth.models import User

from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import FileUploadParser

from faces.models import Face, Comment, Tag, ImageModel
from faces.serializers import UserSerializer, UserGetSerializer, FaceSerializer, FaceGetSerializer, CommentSerializer, TagSerializer, TagGetSerializer, ImageSerializer, RegisterSerializer

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from mfwgallery import authentication

from rest_framework import generics
from rest_framework.permissions import AllowAny

class LoginView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        return Response(self.serializer_class(request.user).data)

# Users can be created without authentication
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

class ImageViewSet(viewsets.ModelViewSet):
    queryset = ImageModel.objects.all()
    serializer_class = ImageSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        serializer = UserGetSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.queryset.get(username=pk)
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

class UserGalleryViewSet(viewsets.ModelViewSet):
    queryset = Face.objects.all()
    serializer_class = FaceGetSerializer

    def list(self, request, user_pk=None):
        user = User.objects.get(username=user_pk)
        queryset = self.queryset.filter(user=user)
        serializer = FaceGetSerializer(queryset, many=True)
        return Response(serializer.data)

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def list(self, request):
        serializer = TagGetSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.queryset.get(pk=pk)
        serializer = TagGetSerializer(queryset)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()    


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

