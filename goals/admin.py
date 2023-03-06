from django.contrib import admin

from goals.models.board import Board, BoardParticipant
from goals.models.goal_comment import GoalComment
from goals.models.goal import Goal
from goals.models.goal_category import GoalCategory


# Register your models here.

@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user__username')


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user__username')


@admin.register(GoalComment)
class GoalCommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'goal', 'created', 'updated')
    search_fields = ('title', 'user__username')


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    list_display_links = ('title',)


@admin.register(BoardParticipant)
class BoardParticipantAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'board_id', 'role')
    list_display_links = ('user_id', 'board_id', 'role')
