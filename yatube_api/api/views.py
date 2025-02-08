# api/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated, AllowAny
from posts.models import Post, Group, Comment, Follow
from api.serializers import PostSerializer
from api.serializers import GroupSerializer
from api.serializers import CommentSerializer
from api.serializers import FollowSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    offset_query_param = 'offset'

    def get_page_size(self, request):
        if request.query_params.get('limit') and \
                request.query_params.get('offset'):
            limit = int(request.query_params.get('limit'))
            offset = int(request.query_params.get('offset'))
            if limit + offset > Post.objects.count():
                return Post.objects.count() - offset
            return limit
        return super().get_page_size(request)

    def paginate_queryset(self, queryset, request, view=None):
        if 'offset' in request.query_params:
            self.offset = int(request.query_params['offset'])
            queryset = queryset[self.offset:]
        return super().paginate_queryset(queryset, request, view)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-pub_date')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = CustomPageNumberPagination  # Используем свой класс

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        # Проверяем, есть ли параметры пагинации в запросе
        if 'limit' in request.query_params or 'offset' in request.query_params:
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            # Если нет, возвращаем просто список
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = None

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        new_queryset = Comment.objects.filter(post_id=post_id)
        return new_queryset

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get("post_id")
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=self.request.user, post=post)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('=following__username',)
    pagination_class = None

    def get_queryset(self):
        new_queryset = Follow.objects.filter(user=self.request.user)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
