import os
from collections.abc import Generator

import pytest
from dotenv import load_dotenv
from playwright.sync_api import APIRequestContext, Playwright

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
