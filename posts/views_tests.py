import pytest

from posts.models import Post


@pytest.mark.django_db
def test_list_all_posts(client, posts, user1, user2):
    response = client.get(
        '/posts',
        HTTP_AUTHORIZATION=f'Bearer {user1.access_token}'     
    )

    assert response.status_code == 200

    data = response.json()

    assert data[0]['text'] == 'First post'
    assert data[0]['user']['username'] == user1.username 

    assert data[1]['text'] == 'Second post'
    assert data[1]['user']['username'] == user1.username 

    assert data[2]['text'] == 'Third post'
    assert data[2]['user']['username'] == user2.username 


@pytest.mark.django_db
def test_create_new_post(client, user1):
    numrows = Post.objects.count()

    data = {'text': 'This is awesome!'}
    response = client.post(
        '/posts', 
        data=data,
        HTTP_AUTHORIZATION=f'Bearer {user1.access_token}'     
    )

    assert response.status_code == 201
    assert Post.objects.count() == numrows+1

    post = response.json()
    assert post['text'] == 'This is awesome!'
    assert post['user']['id'] == user1.id
    assert post['user']['username'] == user1.username
