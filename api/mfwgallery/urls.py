from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.routers import DefaultRouter

from django.contrib import admin
from faces import views

admin.autodiscover()
"""
router = DefaultRouter()
router.register(r'faces', views.GalleryViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'users', views.UserViewSet)
"""
urlpatterns = patterns('',
    url(r'^api/', include('faces.urls')),
    url(r'^api/admin/', include(admin.site.urls)),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

