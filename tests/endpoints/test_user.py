from tests.utils import assert_response


def test_user_me_not_logged(url_for, client):
    url = url_for("user_me")

    response = client.get(url, headers={})

    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}


def test_user_me_invalid_headers(url_for, client):
    url = url_for("user_me")

    response = client.get(url, headers={"Authorization": "Bearer foo"})

    assert response.status_code == 422
    assert_response(response.json(), ["header", "provider"], "field required")


def test_user_me_logged(url_for, client, authenticate_user):
    url = url_for("user_me")

    response = client.get(
        url, headers={"Authorization": "Bearer foo", "Provider": "google"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "first_name": authenticate_user.first_name,
        "last_name": authenticate_user.last_name,
        "email": authenticate_user.email,
        "image": None,
        "is_admin": False,
    }
