from django.conf.urls import patterns, include, url

from django.conf.urls.static import static
from mfwgallery import settings

from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

from posts import views

# Initialize routes
router = routers.SimpleRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'images', views.ImageViewSet)

# Initialize nested routes
users_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'posts', views.UserPostViewSet)

posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', views.CommentViewSet)
posts_router.register(r'tags', views.PostTagViewSet)

# Create URL patterns
urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(posts_router.urls)),
    url(r'^api/', include(users_router.urls)),
    url(r'^api/auth/login/$', views.LoginView.as_view()),
    url(r'^api/auth/register/$', views.RegisterView.as_view()),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

