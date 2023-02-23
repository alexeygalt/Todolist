from django.urls import path

from goals import views
from goals.views.goal import GoalCreateView, GoalListView, GoalView
from goals.views.goal_category import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryView
from goals.views.goal_comment import GoalCommentCreateView, GoalCommentListView, GoalCommentView

urlpatterns = [
    path('goal_category/create', GoalCategoryCreateView.as_view()),
    path('goal_category/list', GoalCategoryListView.as_view()),
    path('goal_category/<pk>', GoalCategoryView.as_view()),

    path('goal/create', GoalCreateView.as_view(), name='goal_create'),
    path('goal/list', GoalListView.as_view(), name='goal_list'),
    path('goal/<pk>', GoalView.as_view(), name='goal_pk'),

    path('goal_comment/create', GoalCommentCreateView.as_view(), name='goal_comment_create'),
    path('goal_comment/list', GoalCommentListView.as_view(), name='goal_comment_list'),
    path('goal_comment/<pk>', GoalCommentView.as_view(), name='goal_comment_pk'),
]
