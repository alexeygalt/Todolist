from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend
from goals.models.goal_category import GoalCategory
from goals.serializers.goal_category import GoalCreateSerializer, GoalCategorySerializer
from rest_framework import filters
from django.db import transaction


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    ordering_fields = ("title", "created",)
    search_fields = ("title",)

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.model.objects.filter(is_deleted=False, user=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance
