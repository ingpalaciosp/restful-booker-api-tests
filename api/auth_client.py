from playwright.sync_api import APIRequestContext, APIResponse


class AuthClient:
    """Cliente de POST /auth. Solo envía peticiones: las comprobaciones van en los tests."""

    RUTA = "/auth"

    def __init__(self, api: APIRequestContext):
        self.api = api

    def pedir_token(self, username: str, password: str) -> APIResponse:
        # data con un diccionario: Playwright lo envía como JSON con Content-Type: application/json
        return self.api.post(self.RUTA, data={"username": username, "password": password})
