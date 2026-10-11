from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch

from app.main import app


client = TestClient(app)


def test_health_returns_200():
    response = client.get("api/v1/health")
    assert response.status_code == 200

def test_ask_without_token_returns_401():
    response = client.post(
        "/api/v1/ask",
        json={"question": "What is a savings account?"}
    )

    assert response.status_code == 401
    assert response.json() == {
        "success": False,
        "error": "Authentication required"
    }
    assert response.headers["www-authenticate"] == "Bearer"

def test_ask_without_rag_role_returns_403():
    claims = {
        "azp": "banking-test-client",
        "aud": ["banking-ai-api"],
        "resource_access": {
            "banking-ai-api": {
                "roles": ["other:role"]
            }
        }
    }

    with patch(
            "app.security.auth.validate_token",
            return_value=claims
    ):
        response = client.post(
            "/api/v1/ask",
            headers={
                "Authorization": "Bearer dummy-token"
            },
            json={
                "question": "What is a savings account?"
            }
        )

    assert response.status_code == 403

    assert response.json() == {
        "success": False,
        "error": "Insufficient permissions"
    }

def test_ask_with_rag_role_returns_200():
    claims = {
        "azp": "banking-test-client",
        "resource_access": {
            "banking-ai-api": {
                "roles": ["rag:ask"]
            }
        }
    }

    with patch(
            "app.security.auth.validate_token",
            return_value=claims
    ), patch(
        "app.api.routes.retrieve_answer",
        return_value="A savings account helps you save money."
    ) as mock_retrieve:

        response = client.post(
            "/api/v1/ask",
            headers={"Authorization": "Bearer dummy-token"},
            json={"question": "What is a savings account?"}
        )

    assert response.status_code == 200
    mock_retrieve.assert_called_once_with("What is a savings account?")

@pytest.mark.parametrize(
    "question",
    [
        pytest.param("Hi" * 500, id="long-question"),
        pytest.param("Hi", id="short-question"),
    ],
)
def test_ask_with_invalid_question_returns_422(question):
    claims = {
        "resource_access": {
            "banking-ai-api": {
                "roles": ["rag:ask"]
            }
        }
    }

    with patch(
            "app.security.auth.validate_token",
            return_value=claims
    ), patch(
        "app.api.routes.retrieve_answer"
    ) as mock_retrieve:

        response = client.post(
            "/api/v1/ask",
            headers={"Authorization": "Bearer dummy-token"},
            json={"question": question}
        )

    assert response.status_code == 422
    mock_retrieve.assert_not_called()

import jwt
from unittest.mock import patch


def test_ask_with_expired_token_returns_401():

    with patch(
            "app.security.auth.validate_token",
            side_effect=jwt.ExpiredSignatureError("Token expired")
    ) as mock_validate:

        response = client.post(
            "/api/v1/ask",
            headers={"Authorization": "Bearer expired-token"},
            json={"question": "What is a savings account?"}
        )

    assert response.status_code == 401

    assert response.json() == {
        "success": False,
        "error": "Invalid or expired token"
    }

    assert response.headers["www-authenticate"] == "Bearer"

    mock_validate.assert_called_once_with("expired-token")

def test_ask_when_rag_service_fails_returns_500():
    claims = {
        "resource_access": {
            "banking-ai-api": {
                "roles": ["rag:ask"]
            }
        }
    }

    with patch(
            "app.security.auth.validate_token",
            return_value=claims
    ), patch(
        "app.api.routes.retrieve_answer",
        side_effect=RuntimeError("Gemini service failed")
    ) as mock_retrieve:

        with TestClient(app, raise_server_exceptions=False) as test_client:
            response = test_client.post(
                "/api/v1/ask",
                headers={"Authorization": "Bearer dummy-token"},
                json={"question": "What is a savings account?"}
            )

    assert response.status_code == 500

    assert response.json() == {
        "success": False,
        "error": "Internal server error"
    }

    mock_retrieve.assert_called_once_with(
        "What is a savings account?"
    )