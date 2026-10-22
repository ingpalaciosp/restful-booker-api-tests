"""Configuración del proyecto: el único sitio donde se lee el entorno (.env)."""

import os

from dotenv import load_dotenv

# Carga el archivo .env si existe. Si no (por ejemplo en el CI), se usan los valores por defecto.
load_dotenv()

# URL de la API
BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")

# Usuario administrador que publica la documentación de Restful-Booker
# (https://restful-booker.herokuapp.com/apidoc/index.html#api-Auth-CreateToken).
USUARIO_ADMIN = os.getenv("API_USERNAME", "admin")
PASSWORD_ADMIN = os.getenv("API_PASSWORD", "password123")
