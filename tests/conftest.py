import typing as t
from contextlib import contextmanager
from pathlib import Path
from time import sleep

import docker
import pytest
from aiohttp.test_utils import unused_port
from docker import DockerClient
from yarl import URL

pytest_plugins: t.Final = (
    "ad_keycloak.pytest_plugin",
)

LOCALHOST: t.Final = "127.0.0.1"

TEST_DIR = Path(__file__).parent


@pytest.fixture(scope="session")
def keycloak(docker_client: DockerClient) -> t.Iterator[URL]:
    dsn = URL.build(
        scheme="http",  # TODO: StrEnum
        host=LOCALHOST,
        port=unused_port(),
    )
    with keycloak_docker_container(dsn, docker_client) as url:
        sleep(15)  # TODO: How to wait service stand up
        yield url


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
            "KEYCLOAK_IMPORT": "/usr/src/app/realm.json",
            "DB_VENDOR": "H2",  # TODO: Maybe to postgres
        },
        volumes={
            str(TEST_DIR): {"bind": "/usr/src/app/", "mode": "ro"},
        },
        ports={
            "8080": (url.host, url.port),
        },
    )
    try:
        yield url
    finally:
        container.remove(force=True)


@pytest.fixture(scope="session")
def docker_client() -> t.Iterator[DockerClient]:
    client = docker.from_env()
    yield client

    client.close()
