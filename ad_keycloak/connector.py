from keycloak import (
    KeycloakDeprecationError,
    KeycloakGetError,
    KeycloakOpenID,
    raise_error_from_response,
)

__all__ = (
    "KeycloakConnector",
)


class KeycloakConnector(KeycloakOpenID):

    def entitlement2(self, token):
        self.connection.add_param_headers("Authorization", "Bearer " + token)

        payload = {
            "grant_type": "urn:ietf:params:oauth:grant-type:uma-ticket",
            "audience": self.client_id,
        }
        params = {
            "realm-name": self.realm_name,
        }

        data_raw = self.connection.raw_post(
            URL_TOKEN.format(**params),
            data=payload,
        )

        if data_raw.status_code == 404:
            return raise_error_from_response(
                data_raw,
                KeycloakDeprecationError,
            )

        return raise_error_from_response(data_raw, KeycloakGetError)


URL_TOKEN = "realms/{realm-name}/protocol/openid-connect/token"
