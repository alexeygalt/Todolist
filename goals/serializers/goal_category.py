from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.serializers import UserRetrieveUpdateSerializer
from goals.models.board import BoardParticipant
from goals.models.goal_category import GoalCategory


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ('id', 'created', 'updated', 'user')
        fields = '__all__'

    def validate(self, attrs):
        role_user = BoardParticipant.objects.filter(
            user=attrs.get('user'),
            board=attrs.get('board'),
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        ).exists()

        if not role_user:
            raise ValidationError("Недостаточно прав")

        return attrs


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserRetrieveUpdateSerializer(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'board')
