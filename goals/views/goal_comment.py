from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from goals.models.goal_comment import GoalComment
from goals.permissions import GoalCommentPermission
from goals.serializers.goal_comment import CreateGoalCommentSerializer, GoalCommentSerializer


class GoalCommentCreateView(CreateAPIView):
    model = GoalComment
    serializer_class = CreateGoalCommentSerializer
    permission_classes = (IsAuthenticated,)


class GoalCommentListView(ListAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (GoalCommentPermission,)
    filter_backends = (
        filters.OrderingFilter,
        DjangoFilterBackend
    )
    filterset_fields = ('goal',)
    ordering = ('-id',)

    def get_queryset(self):
        return self.model.objects.filter(goal__category__board__participants__user=self.request.user)


class GoalCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = (GoalCommentPermission,)

    def get_queryset(self):
        return self.model.objects.filter(goal__category__board__participants__user=self.request.user)
