from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.serializers import UserRetrieveUpdateSerializer
from goals.models.board import BoardParticipant
from goals.models.goal import Goal


class CreateGoalSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')

    def validate(self, attrs):
        role_use = BoardParticipant.objects.filter(
            user=attrs.get('user'),
            board=attrs.get('category').board,
            role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer]
        )

        if not role_use:
            raise ValidationError("Недостаточно прав")

        return attrs


class GoalSerializer(serializers.ModelSerializer):
    user = UserRetrieveUpdateSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError('not allowed in deleted category')

        if value.user != self.context['request'].user:
            raise serializers.ValidationError('not owner of category')

        return value
