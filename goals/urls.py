from django.urls import path

from goals import views
from goals.views.board import BoardCreateView, BoardListView, BoardView
from goals.views.goal import GoalCreateView, GoalListView, GoalView
from goals.views.goal_category import GoalCategoryCreateView, GoalCategoryListView, GoalCategoryView
from goals.views.goal_comment import GoalCommentCreateView, GoalCommentListView, GoalCommentView

urlpatterns = [
    path('goal_category/create', GoalCategoryCreateView.as_view(), name='create_category'),
    path('goal_category/list', GoalCategoryListView.as_view(), name='category_list'),
    path('goal_category/<pk>', GoalCategoryView.as_view(), name='category_pk'),

    path('goal/create', GoalCreateView.as_view(), name='goal_create'),
    path('goal/list', GoalListView.as_view(), name='goal_list'),
    path('goal/<pk>', GoalView.as_view(), name='goal_pk'),

    path('goal_comment/create', GoalCommentCreateView.as_view(), name='goal_comment_create'),
    path('goal_comment/list', GoalCommentListView.as_view(), name='goal_comment_list'),
    path('goal_comment/<pk>', GoalCommentView.as_view(), name='goal_comment_pk'),

    path('board/create', BoardCreateView.as_view(), name='board_create'),
    path('board/list', BoardListView.as_view(), name='board_list'),
    path('board/<pk>', BoardView.as_view(), name='board_pk'),
]
