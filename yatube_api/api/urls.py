# api/urls.py
from django.urls import include, path
from rest_framework import routers
from .views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('posts', PostViewSet)
router_v1.register('groups', GroupViewSet)
router_v1.register(r"posts/(?P<post_id>\d+)/comments", CommentViewSet,
                   basename='comments')
router_v1.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
