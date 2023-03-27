import pytest 


@pytest.mark.django_db
def test_get_current_user_profile(client, user1):
    response = client.get(
        '/account/profile',
        HTTP_AUTHORIZATION=f'Bearer {user1.access_token}'
    )

    assert response.status_code == 200

    data = response.json()
    assert data['name'] == user1.profile.name
    assert data['bio'] == user1.profile.bio
    assert data['website'] == user1.profile.website


@pytest.mark.django_db
def test_update_profile(client, user1):
    data = {
        'name': 'NVIDIA AI',
        'bio': 'Lorem ipsum dolor sit amet',
        'website': 'https://www.nvidia.com',
    }
    response = client.post(
        '/account/profile',
        data=data,
        HTTP_AUTHORIZATION=f'Bearer {user1.access_token}'
    )

    assert response.status_code == 200
    assert response.json() == data

    user1.refresh_from_db()
    user1.profile.refresh_from_db()

    assert user1.profile.name == 'NVIDIA AI'
    assert user1.profile.bio == 'Lorem ipsum dolor sit amet'
    assert user1.profile.website == 'https://www.nvidia.com'
