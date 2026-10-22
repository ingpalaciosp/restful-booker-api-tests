import pytest
from playwright.sync_api import APIRequestContext


@pytest.mark.smoke
def test_la_api_esta_en_marcha(api: APIRequestContext):
    respuesta = api.get("/ping")

    # Restful-Booker responde 201 (no 200) a /ping: así lo indica su documentación.
    assert respuesta.status == 201
