import pytest
from django.urls import reverse

from goals.serializers.board import BoardListSerializer
from tests import factories


@pytest.mark.django_db
def test_list(auth_client, new_user):
    boards = factories.BoardFactory.create_batch(5)
    for board in boards:
        factories.ParticipantFactory.create(board=board, user=new_user)

    response = auth_client.get(f"{reverse('board_list')}?limit=5")

    expected_response = {'count': 5,
                         'next': None,
                         'previous': None,
                         'results': BoardListSerializer(instance=boards, many=True).data}

    assert response.status_code == 200
    assert response.data == expected_response
