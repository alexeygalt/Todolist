import json

import pytest
from django.urls import reverse

from goals.serializers.goal_category import GoalCategorySerializer
from tests import factories


@pytest.mark.django_db
def test_create(auth_client, new_user, board, participant):
    response = auth_client.post(reverse('create_category'),
                                data=json.dumps({'title': 'test_category', 'board': board.pk}),
                                content_type='application/json')

    assert response.status_code == 201


@pytest.mark.django_db
def test_list(auth_client, new_user, board, participant):
    categories = factories.CategoryFactory.create_batch(5, board=board, user=new_user)

    response = auth_client.get(reverse('category_list'))
    expected_response = GoalCategorySerializer(instance=categories, many=True).data

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_retrieve(auth_client, new_user, category, board):
    response = auth_client.get(reverse('category_pk', args=[category.pk]))

    expected_response = {'id': 7,
                         'user': {'id': new_user.pk,
                                  'username': new_user.username,
                                  'first_name': '',
                                  'last_name': '',
                                  'email': new_user.email},
                         'created': response.data.get('created'),
                         'updated': response.data.get('updated'),
                         'title': category.title,
                         'is_deleted': False,
                         'board': board.pk
                         }

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_delete(auth_client, new_user, category):
    response = auth_client.delete(reverse('category_pk', args=[category.pk]))
    assert response.status_code == 204


@pytest.mark.django_db
def test_update(auth_client, new_user, category, board):
    response = auth_client.put(reverse('category_pk', args=[category.pk]),
                               data={'board': board.pk, 'title': 'test name category'})

    assert response.status_code == 200
    assert response.data.get('title') == 'test name category'
