import typing as t

from keycloak import KeycloakOpenID

from ad_auth.provider import Keycloak


def test__keycloak_provider(
    keycloak_resource: KeycloakOpenID,
    tokens: t.Dict,
):
    k = Keycloak(keycloak_resource)
    k.decode(tokens["access_token"])

    app = "ucb:resource:ad_scores"
    perm = "perm:query.score-1"

    assert k.has_perm(app, perm)
    assert not k.has_perm(app, perm="missing")
    assert not k.has_perm(app="missing", perm=perm)
    assert not k.has_perm(app="missing", perm="missing")
