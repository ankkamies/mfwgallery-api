from django.conf.urls import patterns, url
from faces.views import UserViewSet, GalleryViewSet, CommentViewSet, api_root
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns

from faces import views

face_list = GalleryViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

face_detail = GalleryViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

face_comment_list = CommentViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

face_comment_detail = CommentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_list = UserViewSet.as_view({
    'get': 'list'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

urlpatterns = format_suffix_patterns([
    url(r'^$', api_root),
    url(r'^faces/$', face_list, name='face-list'),
    url(r'^faces/(?P<pk>[0-9]+)/$', face_detail, name='face-detail'),
    url(r'^comments/$', face_comment_list, name='face-comment-list'),
    url(r'^comments/(?P<pk>[0-9]+)/$', face_comment_detail, name='face-comment-detail'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
])

