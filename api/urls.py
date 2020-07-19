from django.urls import path, include

from .views import PostViewSet, CommentViewSet, FollowViewSet, GroupViewSet

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'posts/<slug:slug>', PostViewSet)
router.register(
    r'posts/(?P<id>\d+)/comments',
    CommentViewSet,
    basename='CommentSet'
)
router.register(r'follow', FollowViewSet)
router.register(r'group', GroupViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
]
