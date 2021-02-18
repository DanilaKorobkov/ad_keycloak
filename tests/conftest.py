# pylint: disable=redefined-outer-name

import typing as t
from contextlib import contextmanager
from pathlib import Path
from time import sleep

import docker
import pytest
from aiohttp.test_utils import unused_port
from docker import DockerClient
from keycloak import KeycloakOpenID
from keycloak.exceptions import KeycloakConnectionError
from yarl import URL

pytest_plugins: t.Final = (
    "ad_keycloak.pytest_plugin",
)


@pytest.fixture
def tokens(keycloak_client: KeycloakOpenID) -> t.Dict:
    return keycloak_client.token(
        code="bf20271d-9a1d-4ad0-b250-5e6e81a27d33",
        grant_type="client_credentials",
    )


@pytest.fixture(scope="session")
def keycloak_client(keycloak_auth_url: str) -> KeycloakOpenID:
    return KeycloakOpenID(  # nosec - hardcoded_password_funcarg
        server_url=keycloak_auth_url,
        realm_name="demo",
        client_id="ext:client_type:tinkoff",
        client_secret_key="bf20271d-9a1d-4ad0-b250-5e6e81a27d33",
    )


@pytest.fixture(scope="session")
def keycloak_resource(keycloak_auth_url: str) -> KeycloakOpenID:
    return KeycloakOpenID(
        server_url=keycloak_auth_url,
        client_id="ucb:resource:ad_scores",
        realm_name="demo",
    )


@pytest.fixture(scope="session")
def keycloak_auth_url(keycloak: URL) -> str:
    return f"{keycloak}/auth/"


@pytest.fixture(scope="session")
def keycloak(docker_client: DockerClient) -> t.Iterator[URL]:
    dsn = URL.build(
        scheme="http",
        host=LOCALHOST,
        port=unused_port(),
    )
    with keycloak_docker_container(dsn, docker_client) as url:
        auth_utl = f"{url}/auth/"

        k = KeycloakOpenID(auth_utl, realm_name="demo", client_id="")
        wait_setup(k)

        yield url


@pytest.fixture(scope="session")
def docker_client() -> t.Iterator[DockerClient]:
    client = docker.from_env()
    yield client

    client.close()


def wait_setup(keycloak: KeycloakOpenID) -> None:
    for _ in range(100):
        try:
            keycloak.public_key()
        except KeycloakConnectionError:
            sleep(0.5)
        else:
            return

    raise RuntimeError


@contextmanager
def keycloak_docker_container(
    url: URL,
    docker_client: DockerClient,
) -> t.Iterator[URL]:
    container = docker_client.containers.run(
        image="jboss/keycloak:12.0.2",
        auto_remove=True,
        detach=True,
        environment={
            "KEYCLOAK_PASSWORD": "admin",
            "KEYCLOAK_USER": "admin",
            "KEYCLOAK_IMPORT": "/app/realm.json",
            "DB_VENDOR": "H2",
        },
        volumes={
            str(TESTS_DIR): {"bind": "/app", "mode": "ro"},
        },
        ports={
            "8080": (url.host, url.port),
        },
    )
    try:
        yield url
    finally:
        container.remove(force=True)


LOCALHOST: t.Final = "127.0.0.1"
TESTS_DIR: t.Final = Path(__file__).parent
