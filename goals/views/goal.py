from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from goals.filters import GoalDateFilter
from goals.models.goal import Goal
from goals.permissions import GoalPermission
from goals.serializers.goal import CreateGoalSerializer, GoalSerializer


class GoalCreateView(CreateAPIView):
    model = Goal
    serializer_class = CreateGoalSerializer
    permission_classes = (IsAuthenticated,)


class GoalListView(ListAPIView):
    model = Goal
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (GoalPermission,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ('-priority', 'due_day',)
    ordering = ('-priority',)
    search_fields = ('title',)

    def get_queryset(self):
        return self.model.objects.filter(category__board__participants__user=self.request.user)


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = (GoalPermission,)

    def get_queryset(self):
        return self.model.objects.filter(category__board__participants__user=self.request.user)

    def perform_destroy(self, instance):
        """
        При удалении цели у нее меняется поле статус на "В архиве"
        """
        instance.status = self.model.Status.archived
        instance.save()
        return instance
