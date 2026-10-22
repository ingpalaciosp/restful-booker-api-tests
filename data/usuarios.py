import os

# Usuario administrador que publica la documentación de Restful-Booker
# (https://restful-booker.herokuapp.com/apidoc/index.html#api-Auth-CreateToken).
# Se pueden sobrescribir con las variables de entorno API_USERNAME y API_PASSWORD.
USUARIO_ADMIN = os.getenv("API_USERNAME", "admin")
PASSWORD_ADMIN = os.getenv("API_PASSWORD", "password123")
