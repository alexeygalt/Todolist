import pytest
from django.urls import reverse

from goals.serializers.goal_comment import GoalCommentSerializer
from tests import factories


@pytest.mark.django_db
def test_create(auth_client, new_user, goal):
    response = auth_client.post(reverse('goal_comment_create'),
                                data={'text': 'test comment', 'goal': goal.pk})

    expected_response = {'id': response.data.get('id'),
                         'created': response.data.get('created'),
                         'updated': response.data.get('updated'),
                         'text': 'test comment',
                         'goal': goal.pk}

    assert response.status_code == 201
    assert response.data == expected_response


@pytest.mark.django_db
def test_list(auth_client, new_user, goal):
    comments = factories.CommentFactory.create_batch(5, goal=goal, user=new_user)
    response = auth_client.get(reverse('goal_comment_list'))
    expected_response = GoalCommentSerializer(instance=comments, many=True).data
    expected_response = sorted(expected_response, key=lambda x: x['id'], reverse=True)

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_retrieve(auth_client, new_user, comment, goal):
    response = auth_client.get(reverse('goal_comment_pk', args=[comment.pk]))

    expected_response = {'id': response.data.get('id'),
                         'user': {'id': new_user.pk,
                                  'username': 'testname',
                                  'first_name': '',
                                  'last_name': '',
                                  'email': 'test@mail.ru'},
                         'created': response.data.get('created'),
                         'updated': response.data.get('updated'),
                         'text': comment.text,
                         'goal': goal.pk}

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_update(auth_client, new_user, comment):
    response = auth_client.put(reverse('goal_comment_pk', args=[comment.pk]),
                               data={'text': 'test text update'})

    assert response.status_code == 200
    assert response.data.get('text') == 'test text update'


@pytest.mark.django_db
def test_delete(auth_client, new_user, comment):
    response = auth_client.delete(reverse('goal_comment_pk', args=[comment.pk]))

    assert response.status_code == 204
