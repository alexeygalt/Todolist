from rest_framework import serializers

from core.serializers import UserRetrieveUpdateSerializer
from goals.models.goal_comment import GoalComment


class CreateGoalCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')

    def validate_category(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError('not owner of category')

        return value


class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserRetrieveUpdateSerializer(read_only=True)

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'goal')

    def validate_category(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError('not owner of category')

        return value
