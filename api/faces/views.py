from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from faces.models import Face, Comment
from faces.serializers import UserSerializer, FaceSerializer, CommentSerializer

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'faces': reverse('face-list', request=request, format=format),
        'comments': reverse('face-comment-list', request=request, format=format),
        })

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()

class GalleryViewSet(viewsets.ModelViewSet):
    queryset = Face.objects.all()
    serializer_class = FaceSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, face_pk=None):
        queryset = self.queryset.filter(face=face_pk)
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, face_pk=None):
        queryset = self.queryset.get(pk=pk, face=face_pk)
        serializer = CommentSerializer(queryset)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

