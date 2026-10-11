import os

import jwt
from dotenv import load_dotenv
from jwt import PyJWKClient

load_dotenv()


def get_config(config_key: str) -> str:
    config_value = os.getenv(config_key)
    if not config_value:
        raise ValueError(f"{config_key} configration is missing")
    return config_value


keycloak_issuer = get_config("KEYCLOAK_ISSUER")
keycloak_audience = get_config("KEYCLOAK_AUDIENCE")
JWKS_URL = f"{keycloak_issuer}{get_config("JWKS_URL_SUFFIX")}"

jwk_client = PyJWKClient(JWKS_URL)


def validate_token(token: str) -> dict:
    signing_key = jwk_client.get_signing_key_from_jwt(token)

    claims = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience=keycloak_audience,
        issuer=keycloak_issuer,
        options={"require": ["exp", "iss", "aud"]},
    )

    return claims
