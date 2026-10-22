# Pruebas de API de Restful-Booker

Pruebas automatizadas de la API de [Restful-Booker](https://restful-booker.herokuapp.com), una API de reservas de hotel creada para practicar testing.

## Qué se prueba

| Funcionalidad | Casos | Tests |
|---|---|---|
| Disponibilidad (`/ping`) | — | `tests/test_ping.py` |
| Pedir token (`POST /auth`) | [`casos/auth.md`](casos/auth.md) | pendiente |

## Tecnologías

- **Python** y **pytest**
- **Playwright** (`APIRequestContext`) para enviar las peticiones HTTP, sin navegador
- **jsonschema** para validar la estructura (contrato) de las respuestas
- **Faker** para generar datos de prueba realistas y únicos
- **python-dotenv** para leer la configuración desde un archivo `.env`
- **Ruff** para revisar el estilo y los errores comunes del código
- **pytest-html** para el informe
- **GitHub Actions** para ejecutar los tests en cada cambio

## Estructura

```
config/              configuración: el único sitio donde se lee el .env (URL y credenciales)
api/                 clientes de la API: un archivo por endpoint (envían peticiones, no comprueban)
schemas/             contratos JSON Schema de las respuestas
data/                datos de prueba (payloads para crear o modificar reservas)
tests/               tests automatizados y fixtures (conftest.py)
casos/               casos de prueba escritos antes de automatizar
http/                peticiones para probar a mano con la extensión REST Client de VS Code
docs/                documentación del proyecto
.github/workflows/   pipeline de CI (GitHub Actions)
```

Flujo de trabajo: probar a mano (`http/`) → escribir los casos (`casos/`) → automatizarlos (`tests/`, usando `api/`, `schemas/` y `data/`).

## Cómo ejecutarlo

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
copy .env.example .env      # opcional: solo si quieres cambiar la URL o las credenciales
pytest -v
```

Otras formas útiles:

```powershell
pytest -m smoke                                   # solo las comprobaciones rápidas
pytest --html=informe.html --self-contained-html  # genera el informe HTML
ruff check . ; ruff format .                      # revisa y ordena el código
```

## Configuración

| Variable | Para qué sirve | Valor por defecto |
|---|---|---|
| `BASE_URL` | URL de la API | `https://restful-booker.herokuapp.com` |
| `API_USERNAME` | Usuario para pedir el token | `admin` |
| `API_PASSWORD` | Contraseña para pedir el token | `password123` |

El archivo `.env` no se sube a git; `.env.example` sirve de plantilla.
