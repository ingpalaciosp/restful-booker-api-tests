from collections.abc import Generator

import pytest
from playwright.sync_api import APIRequestContext, Playwright

from api.auth_client import AuthClient
from config import settings


@pytest.fixture(scope="session")
def base_url(pytestconfig: pytest.Config) -> str:
    """URL de la API: la de --base-url si se pasa al ejecutar; si no, la de config/settings.py."""
    return pytestconfig.getoption("base_url") or settings.BASE_URL


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
    respuesta = auth_client.pedir_token(settings.USUARIO_ADMIN, settings.PASSWORD_ADMIN)
    cuerpo = respuesta.json()
    # Restful-Booker responde 200 incluso con credenciales incorrectas: hay que mirar el body.
    assert "token" in cuerpo, f"No se pudo obtener el token: {cuerpo}"
    return cuerpo["token"]
