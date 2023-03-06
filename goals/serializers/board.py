from django.db import transaction
from rest_framework import serializers

from core.models import User
from goals.models.board import Board, BoardParticipant


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ('id', 'created', 'updated')
        fields = '__all__'

    def create(self, validated_data):
        user = validated_data.pop('user')
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.Role.choices
    )
    user = serializers.SlugRelatedField(
        slug_field='username', queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'board')


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated')

    def update(self, instance, validated_data):
        owner = validated_data.pop('user')
        new_participant = validated_data.pop('participants')
        new_by_part = {item['user'].id: item for item in new_participant}

        old_participants = instance.participants.exclude(user=owner)

        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_by_part:
                    old_participant.delete()
                else:
                    if old_participant.role != new_by_part[old_participant.user_id]['role']:
                        old_participant.role = new_by_part[old_participant.user_id]['role']
                        old_participant.save()

                    new_by_part.pop(old_participant.user_id)

            for new_part in new_by_part.values():
                BoardParticipant.objects.create(
                    board=instance, user=new_part['user'], role=new_part['role']
                )

            instance.title = validated_data['title']
            instance.save()

        return instance
