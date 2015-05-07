from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from django.contrib import admin
from faces import views

admin.autodiscover()

router = routers.SimpleRouter()
router.register(r'faces', views.GalleryViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'users', views.UserViewSet)

faces_router = routers.NestedSimpleRouter(router, r'faces', lookup='face')
faces_router.register(r'comments', views.CommentViewSet)

urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(faces_router.urls)),
    url(r'^api/admin/', include(admin.site.urls)),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

