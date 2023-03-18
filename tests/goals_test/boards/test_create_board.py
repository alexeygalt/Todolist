import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_create(auth_client):
    response = auth_client.post(reverse('board_create'),
                                data={'title': 'test_board'})
    expected_response = {'id': response.data['id'],
                         'created': response.data.get('created'),
                         'updated': response.data.get('updated'),
                         'title': 'test_board',
                         'is_deleted': False, }

    assert response.status_code == 201
    assert response.data == expected_response
