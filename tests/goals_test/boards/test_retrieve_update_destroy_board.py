import json

import pytest
from django.urls import reverse


from goals.serializers.board import BoardSerializer


@pytest.mark.django_db
def test_retrieve(auth_client, new_user, board, participant):
    response = auth_client.get(reverse('board_pk', args=[board.pk]))

    expected_response = BoardSerializer(instance=board).data

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_delete(auth_client, new_user, board, participant):
    response = auth_client.delete(reverse('board_pk', args=[board.pk]))

    assert response.status_code == 204


@pytest.mark.django_db
def test_update(auth_client, new_user, board, participant):
    response = auth_client.put(reverse('board_pk', args=[board.pk]),
                               data=json.dumps({'title': 'put test title', 'participants': []}),
                               content_type='application/json')

    assert response.status_code == 200
    assert response.data.get('title') == 'put test title'
