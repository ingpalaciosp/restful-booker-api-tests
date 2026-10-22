# Contratos (JSON Schema) de las respuestas de POST /auth.
# Se comprueban en los tests con jsonschema.validate(respuesta.json(), TOKEN).

# Respuesta correcta según la documentación: {"token": "abc123"}
TOKEN = {
    "type": "object",
    "properties": {
        "token": {"type": "string", "minLength": 1},
    },
    "required": ["token"],
    "additionalProperties": False,
}
