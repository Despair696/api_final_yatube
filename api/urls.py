from django.urls import path, include

from .views import PostViewSet, CommentViewSet, FollowViewSet, GroupViewSet

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )


router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(r'follow', FollowViewSet)
router.register(r'group', GroupViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path(
        'api/v1/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/v1/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
