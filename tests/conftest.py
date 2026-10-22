import os
from collections.abc import Generator

import pytest
from dotenv import load_dotenv
from playwright.sync_api import APIRequestContext, Playwright

from api.auth_client import AuthClient

# Carga las variables del archivo .env (si existe) antes de que se importen los tests.
load_dotenv()


@pytest.fixture(scope="session")
def base_url(pytestconfig: pytest.Config) -> str:
    """URL de la API: BASE_URL del entorno, o si no, la de pytest.ini / --base-url."""
    return os.getenv("BASE_URL") or pytestconfig.getoption("base_url")


@pytest.fixture(scope="session")
def api(playwright: Playwright, base_url: str) -> Generator[APIRequestContext]:
    """Cliente de API: envía peticiones a base_url sin abrir ningún navegador."""
    contexto = playwright.request.new_context(
        base_url=base_url,
        extra_http_headers={"Accept": "application/json"},
    )
    yield contexto
    contexto.dispose()


@pytest.fixture(scope="session")
def auth_client(api: APIRequestContext) -> AuthClient:
    return AuthClient(api)


@pytest.fixture(scope="session")
def token(auth_client: AuthClient) -> str:
    """Token de admin, pedido una sola vez para toda la sesión de tests."""
    # Se importa aquí para que load_dotenv() ya haya cargado el .env.
    from data.usuarios import PASSWORD_ADMIN, USUARIO_ADMIN

    respuesta = auth_client.pedir_token(USUARIO_ADMIN, PASSWORD_ADMIN)
    cuerpo = respuesta.json()
    # Restful-Booker responde 200 incluso con credenciales incorrectas: hay que mirar el body.
    assert "token" in cuerpo, f"No se pudo obtener el token: {cuerpo}"
    return cuerpo["token"]
