import typing as t

import pytest
from keycloak import KeycloakOpenID

from ad_keycloak import KeycloakClient, PermissionDenied, Token

TEST_APP: t.Final = "ucb:resource:ad_scores"
TEST_PERM: t.Final = "perm:query.score-1"


async def test__validate__if_ok_return_token(
    keycloak_resource: KeycloakOpenID,
    tokens: t.Dict,
):
    k = KeycloakClient(keycloak_resource)

    token = await k.validate(tokens["access_token"], TEST_APP, TEST_PERM)
    assert isinstance(token, Token)


@pytest.mark.parametrize(
    "app, perm",
    (
        (TEST_APP, "missing"),
        ("missing", TEST_PERM),
        ("missing", "missing"),
    ),
)
async def test__validate__permission_denied(
    keycloak_resource: KeycloakOpenID,
    tokens: t.Dict,
    app: str,
    perm: str,
):
    k = KeycloakClient(keycloak_resource)

    with pytest.raises(PermissionDenied) as e:
        await k.validate(tokens["access_token"], app, perm)

    assert e.value.app == app
    assert e.value.perm == perm
