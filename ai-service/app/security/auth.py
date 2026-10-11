import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import PyJWKClientError, PyJWKClientConnectionError

from app.security.jwt_validator import validate_token


bearer_scheme = HTTPBearer(auto_error=False)


def require_rag_ask(
        credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:

    # Step 1: Check whether a Bearer token was provided
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Step 2: Validate the JWT
    try:
        claims = validate_token(credentials.credentials)

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except (PyJWKClientError, PyJWKClientConnectionError):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service temporarily unavailable",
        )

    # Step 3: Extract roles from the verified JWT
    roles = (
        claims.get("resource_access", {})
        .get("banking-ai-api", {})
        .get("roles", [])
    )

    # Step 4: Check authorization
    if "rag:ask" not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions",
        )

    # Step 5: Return verified claims
    return claims