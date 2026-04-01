import io

import pytest
from PIL import Image
from starlette.testclient import TestClient
from app.schemas.auth import AuthResponse


@pytest.fixture(name="user_data")
def user_data() -> dict[str, str]:
    return {
        "username": "testfollowuser",
        "email": "testfollow@example.com",
        "password": "supermegapasswordyipi"
    }

@pytest.fixture(name="client_data")
def client_data() -> dict[str, str]:
    return {
        "username": "testfollowclient",
        "email": "clientfollow@example.com",
        "password": "supermegapasswordyipi"
    }

@pytest.fixture(name="registered_user")
def registered_user(client: TestClient, user_data: dict[str, str]) -> dict[str, str]:
    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 200
    return user_data


@pytest.fixture(name="authenticated_user")
def authenticated_user(client: TestClient, registered_user: dict[str, str]) -> AuthResponse:
    response = client.post("/auth/login", json={
        "username": registered_user["username"],
        "password": registered_user["password"]
    })

    assert response.status_code == 200
    assert "token" in response.json()
    return AuthResponse(**response.json())

@pytest.fixture(name="auth_token")
def auth_token(authenticated_user: AuthResponse) -> str:
    """Fixture qui retourne uniquement le token d'authentification."""
    return authenticated_user.token


@pytest.fixture(name="auth_headers")
def auth_headers(auth_token: str) -> dict[str, str]:
    """Fixture qui retourne les headers d'authentification prets à utiliser."""
    return {"Authorization": f"Bearer {auth_token}"}

@pytest.fixture
def picture(filename="test-like.png"):
    file = io.BytesIO()
    image = Image.new("RGB", (10, 10), color="white")
    image.save(file, "JPEG")
    file.seek(0)
    return {
        "file": (filename, file, "image/jpeg")
    }


@pytest.fixture
def created_post(client: TestClient, auth_headers: dict, picture: dict):
    response = client.post(
        "/post/upload",
        headers=auth_headers,
        data={"caption": "Post pour test like"},
        files=picture,
    )
    assert response.status_code == 200
    return response.json()


def test_like_post(client: TestClient, auth_headers: dict, created_post: dict):
    response = client.post(f"/like/{created_post['id']}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["post_id"] == created_post["id"]
    assert "id" in data
    assert "created_at" in data


def test_like_post_twice_should_fail(client: TestClient, auth_headers: dict, created_post: dict):
    client.post(f"/like/{created_post['id']}", headers=auth_headers)
    response = client.post(f"/like/{created_post['id']}", headers=auth_headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "You have already liked this post"


def test_unlike_post(client: TestClient, auth_headers: dict, created_post: dict):
    # Liker d'abord
    client.post(f"/like/{created_post['id']}", headers=auth_headers)
    # Ensuite unliker
    response = client.delete(f"/like/{created_post['id']}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["post_id"] == created_post["id"]
    assert "id" in data
    assert "user_id" in data


def test_get_liked_posts_by_user(client: TestClient, auth_headers: dict, authenticated_user: AuthResponse, created_post: dict):
    client.post(f"/like/{created_post['id']}", headers=auth_headers)

    response = client.get(f"/like/liked-posts/{authenticated_user.user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == authenticated_user.user_id
    assert isinstance(data["liked_posts"], list)
    assert any(p["id"] == created_post["id"] for p in data["liked_posts"])


def test_get_post_likes(client: TestClient, auth_headers: dict, created_post: dict):
    client.post(f"/like/{created_post['id']}", headers=auth_headers)

    response = client.get(f"/like/get-likes/{created_post['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["post_id"] == created_post["id"]
    assert data["likes_count"] == 1
    assert isinstance(data["users"], list)
    assert len(data["users"]) == 1
    assert "username" in data["users"][0]
