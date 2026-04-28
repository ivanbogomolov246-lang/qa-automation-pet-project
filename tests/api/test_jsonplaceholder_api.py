import pytest


@pytest.mark.api
@pytest.mark.parametrize(
    "path, expected_keys",
    [
        ("/users/1", ["id", "name", "email"]),
        ("/posts/1", ["id", "title", "body", "userId"]),
    ],
)
def test_get_resource_by_id(api_client, path, expected_keys):
    # GET should return 200 and expected fields.
    response = api_client.get(path)

    assert response.status_code == 200
    body = response.json()
    for key in expected_keys:
        assert key in body


@pytest.mark.api
@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_get_posts_by_user_id(api_client, user_id):
    # Validate filtering by query parameter.
    response = api_client.get("/posts", params={"userId": user_id})

    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert len(posts) > 0
    assert all(post["userId"] == user_id for post in posts)


@pytest.mark.api
@pytest.mark.parametrize(
    "payload",
    [
        {"title": "QA auto test", "body": "Create post scenario", "userId": 1},
        {"title": "Second post", "body": "Validation example", "userId": 7},
    ],
)
def test_create_post(api_client, payload):
    # Validate POST: status 201 and payload echoed in response body.
    response = api_client.post("/posts", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == payload["title"]
    assert body["body"] == payload["body"]
    assert body["userId"] == payload["userId"]
    assert "id" in body


@pytest.mark.api
@pytest.mark.parametrize("path", ["/users/0", "/posts/0", "/unknown-endpoint"])
def test_negative_unknown_resource(api_client, path):
    # Negative case: unknown path should return 404.
    response = api_client.get(path)
    assert response.status_code == 404


@pytest.mark.api
def test_negative_posts_for_unknown_user_returns_empty_list(api_client):
    # Negative case: valid path but non-existing userId.
    response = api_client.get("/posts", params={"userId": 99999})

    assert response.status_code == 200
    assert response.json() == []
