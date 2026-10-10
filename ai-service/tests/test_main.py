import json
from unittest.mock import Mock, patch

import pytest
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.main import http_exception_handler, validation_exception_handler, generic_exception_handler
from app.model.chat import AskRequest


def test_http_exception_handler():

    # Arrange
    request = Mock()

    exception = StarletteHTTPException(
        status_code=404,
        detail="Resource not found"
    )

    # Act
    response = http_exception_handler(request, exception)

    # Assert
    assert response.status_code == 404
    assert response.body == (
        b'{"success":false,"error":"Resource not found"}'
    )

def test_validation_exception_handler():

    # Arrange
    request = Mock()

    with pytest.raises(ValidationError) as exc_info:
        AskRequest(question="  Hi  ")

    exception = RequestValidationError(
        exc_info.value.errors()
    )

    # Act
    response = validation_exception_handler(request, exception)

    # Assert
    assert response.status_code == 422

    body = json.loads(response.body)

    assert body["success"] is False
    assert body["error"] == "Validation error"
    assert body["details"][0]["type"] == "string_too_short"

def test_generic_exception_handler():

    # Arrange
    request = Mock()
    exception = RuntimeError("Database password is invalid")

    # Mock the logger used inside app.main
    with patch("app.main.logger") as mock_logger:

        # Act
        response = generic_exception_handler(request, exception)

        # Assert
        assert response.status_code == 500

        body = json.loads(response.body)

        assert body["success"] is False
        assert body["error"] == "Internal server error"

        # Sensitive exception details must not reach the client
        assert "Database password" not in response.body.decode()

        # Verify logging
        mock_logger.exception.assert_called_once_with(
            "Unhandled exception occurred"
        )