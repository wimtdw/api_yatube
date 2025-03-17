from rest_framework.routers import SimpleRouter
from django.urls import include, path
from .views import PostViewSet, GroupViewSet, CommentViewSet


router = SimpleRouter()
router.register('posts', PostViewSet, basename='post')
router.register('groups', GroupViewSet, basename='group')
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/', include(router.urls)),
]
