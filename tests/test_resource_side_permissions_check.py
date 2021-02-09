from yarl import URL

from ad_keycloak import KeycloakConnector


def test__permissions_from_token(keycloak: URL):
    # client side
    server_url = f"{keycloak}/auth/"

    keycloak_client = KeycloakConnector(
        server_url=server_url,
        realm_name="demo",
        client_id="ext:client_type:tinkoff",
        client_secret_key="bf20271d-9a1d-4ad0-b250-5e6e81a27d33",
    )
    tokens = keycloak_client.token("user", "password")
    access_token = tokens["access_token"]

    # server side (ucb:resource:ad_scores)
    resource_service = KeycloakConnector(
        server_url=server_url,
        client_id="ucb:resource:ad_scores",
        realm_name="demo",
    )

    public_key = resource_service.public_key()
    public_key = get_wrapped_public_key(public_key)

    options = {
        "verify_signature": True,
        "verify_aud": False,
        "verify_exp": True,
    }
    token_info = keycloak_client.decode_token(
        access_token,
        key=public_key,
        options=options,
    )

    permissions = token_info["resource_access"]
    # check user can access here
    assert permissions["ucb:resource:ad_scores"] == {
        "roles": ["perm:query.score-1"],
    }


def get_wrapped_public_key(key: str) -> str:
    return f"-----BEGIN PUBLIC KEY-----\n{key}\n-----END PUBLIC KEY-----"
