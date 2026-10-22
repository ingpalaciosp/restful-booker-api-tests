# Auth (pedir token)

## Datos y estados de partida

- URL: `https://restful-booker.herokuapp.com` · Endpoint: `POST /auth`
- Documentación: [CreateToken](https://restful-booker.herokuapp.com/apidoc/index.html#api-Auth-CreateToken)
- Datos válidos de referencia: usuario `admin`, contraseña `password123`
- **Header de referencia**: `Content-Type: application/json`
- **Reserva propia**: una reserva creada con `POST /booking` para este caso (no usar reservas de otras personas), con `firstname` `Ana`.
- Limpieza: borrar la reserva propia al terminar (`DELETE /booking/{id}` con el token).

Qué dice la documentación (requisito):
- `username` y `password` son obligatorios y de tipo texto.
- El header `Content-Type: application/json` es obligatorio.
- Si todo va bien: `200` y `{"token": "..."}`.
- El token sirve para usar `PUT` y `DELETE` en `/booking`.
- **No define qué responder ante un error.** Esos casos usan criterio QA según el estándar HTTP (`401` credenciales incorrectas, `400` petición mal formada, `415` formato no indicado) y están en "Preguntas para el PO".

## Credenciales válidas

| Id | Caso | Prioridad | Precondiciones | Procedimiento | Esperado | Obtenido | Notas |
|---|---|---|---|---|---|---|---|
| TC-AUTH-001 | Pedir token con credenciales válidas | 🔴 Alta | N/A | 1. Enviar `POST /auth` con el header de referencia y body `{"username": "admin", "password": "password123"}` | Debería responder `200` con un campo `token` de texto no vacío | ✅ Responde `200` y `{"token": "64c893f0b1977f6"}` | Req: documentación CreateToken |
| TC-AUTH-002 | El token permite modificar una reserva | 🔴 Alta | 1. Reserva propia creada<br>2. Token obtenido con TC-AUTH-001 | 1. Enviar `PATCH /booking/{id}` de la reserva propia con el header de referencia, `Cookie: token=<token>` y body `{"firstname": "Lucia"}` | Debería responder `200` con `firstname` `Lucia` | ✅ Responde `200` y la reserva devuelve `"firstname": "Lucia"` | Req: documentación CreateToken ("access to the PUT and DELETE /booking") |
| TC-AUTH-003 | La respuesta viene en JSON | 🟢 Baja | N/A | 1. Enviar `POST /auth` con el header de referencia y body `{"username": "admin", "password": "password123"}` | Debería responder con el header `Content-Type` `application/json` | ✅ `Content-Type: application/json; charset=utf-8` | Req: ejemplo de respuesta de la documentación (JSON) |
| TC-AUTH-004 | Token nuevo en cada petición | 🟢 Baja | N/A | 1. Enviar `POST /auth` con el header de referencia y body `{"username": "admin", "password": "password123"}`<br>2. Repetir el paso 1<br>3. Comparar los dos `token` | A confirmar | 🔍 Los tokens son distintos (`64c893f0b1977f6` y `3774f1a07fc1961`) | Comportamiento actual: cada petición devuelve un token nuevo<br>A confirmar: ¿el token anterior sigue siendo válido? ¿Caduca? |

## Credenciales incorrectas

| Id | Caso | Prioridad | Precondiciones | Procedimiento | Esperado | Obtenido | Notas |
|---|---|---|---|---|---|---|---|
| TC-AUTH-005 | Contraseña incorrecta | 🔴 Alta | N/A | 1. Enviar `POST /auth` con el header de referencia y body `{"username": "admin", "password": "incorrecta"}` | Debería responder `401` y no devolver `token` | ❌ Responde `200` con `{"reason": "Bad credentials"}`; no devuelve `token` | Req: criterio QA (estándar HTTP), validar con PO<br>Bug: pendiente |
| TC-AUTH-006 | Usuario inexistente | 🔴 Alta | N/A | 1. Enviar `POST /auth` con el header de referencia y body `{"username": "noexiste", "password": "password123"}` | Debería responder `401` y no devolver `token` | ❌ Responde `200` con `{"reason": "Bad credentials"}`; no devuelve `token` | Req: criterio QA (estándar HTTP), validar con PO<br>Bug: pendiente (mismo que TC-AUTH-005) |
| TC-AUTH-007 | Contraseña vacía | 🟡 Media | N/A | 1. Enviar `POST /auth` con el header de referencia y body `{"username": "admin", "password": ""}` | Debería responder `401` y no devolver `token` | ❌ Responde `200` con `{"reason": "Bad credentials"}`; no devuelve `token` | Req: criterio QA (estándar HTTP), validar con PO<br>Bug: pendiente (mismo que TC-AUTH-005) |
| TC-AUTH-008 | Usuario vacío | 🟡 Media | N/A | 1. Enviar `POST /auth` con el header de referencia y body `{"username": "", "password": "password123"}` | Debería responder `401` y no devolver `token` | ❌ Responde `200` con `{"reason": "Bad credentials"}`; no devuelve `token` | Req: criterio QA (estándar HTTP), validar con PO<br>Bug: pendiente (mismo que TC-AUTH-005) |
| TC-AUTH-009 | Contraseña en mayúsculas | 🟡 Media | N/A | 1. Enviar `POST /auth` con el header de referencia y body `{"username": "admin", "password": "PASSWORD123"}` | Debería responder `401` y no devolver `token` | ❌ Responde `200` con `{"reason": "Bad credentials"}`; no devuelve `token` | Req: criterio QA (estándar HTTP), validar con PO. La contraseña distingue mayúsculas (correcto)<br>Bug: pendiente (mismo que TC-AUTH-005) |
| TC-AUTH-010 | Inyección SQL en las credenciales | 🟡 Media | N/A | 1. Enviar `POST /auth` con el header de referencia y body `{"username": "admin' OR '1'='1", "password": "x' OR '1'='1"}` | Debería responder `401` y no devolver `token` | ❌ Responde `200` con `{"reason": "Bad credentials"}`; no devuelve `token` | Req: criterio QA (estándar HTTP), validar con PO. No entra con la inyección (correcto)<br>Bug: pendiente (mismo que TC-AUTH-005) |
| TC-AUTH-011 | Usuario en mayúsculas | 🟢 Baja | N/A | 1. Enviar `POST /auth` con el header de referencia y body `{"username": "ADMIN", "password": "password123"}` | A confirmar | 🔍 Responde `200` con `{"reason": "Bad credentials"}`; no devuelve `token` | Comportamiento actual: el usuario distingue mayúsculas<br>A confirmar: ¿`ADMIN` y `admin` deben ser el mismo usuario? |
| TC-AUTH-012 | Usuario con espacios delante y detrás | 🟢 Baja | N/A | 1. Enviar `POST /auth` con el header de referencia y body `{"username": " admin ", "password": "password123"}` | A confirmar | 🔍 Responde `200` con `{"reason": "Bad credentials"}`; no devuelve `token` | Comportamiento actual: no ignora los espacios<br>A confirmar: ¿deben ignorarse los espacios? |

## Petición mal formada

| Id | Caso | Prioridad | Precondiciones | Procedimiento | Esperado | Obtenido | Notas |
|---|---|---|---|---|---|---|---|
| TC-AUTH-013 | Body vacío | 🟡 Media | N/A | 1. Enviar `POST /auth` con el header de referencia y body `{}` | Debería responder `400` y no devolver `token` | ❌ Responde `200` con `{"reason": "Bad credentials"}`; no devuelve `token` | Req: campos obligatorios según la documentación; código: criterio QA, validar con PO<br>Bug: pendiente (mismo que TC-AUTH-005) |
| TC-AUTH-014 | Falta el campo `username` | 🟡 Media | N/A | 1. Enviar `POST /auth` con el header de referencia y body `{"password": "password123"}` | Debería responder `400` y no devolver `token` | ❌ Responde `200` con `{"reason": "Bad credentials"}`; no devuelve `token` | Req: campo obligatorio según la documentación; código: criterio QA, validar con PO. Cubre también el campo mal escrito (`"usuario"` en vez de `"username"`)<br>Bug: pendiente (mismo que TC-AUTH-005) |
| TC-AUTH-015 | Falta el campo `password` | 🟡 Media | N/A | 1. Enviar `POST /auth` con el header de referencia y body `{"username": "admin"}` | Debería responder `400` y no devolver `token` | ❌ Responde `200` con `{"reason": "Bad credentials"}`; no devuelve `token` | Req: campo obligatorio según la documentación; código: criterio QA, validar con PO<br>Bug: pendiente (mismo que TC-AUTH-005) |
| TC-AUTH-016 | Sin header `Content-Type` | 🟡 Media | N/A | 1. Enviar `POST /auth` sin header `Content-Type` y con body `{"username": "admin", "password": "password123"}` | Debería responder `415` y no devolver `token` | ❌ Responde `200` con `{"reason": "Bad credentials"}`; no devuelve `token` | Req: header obligatorio según la documentación; código: criterio QA, validar con PO. El mensaje confunde: las credenciales eran correctas<br>Bug: pendiente (mismo que TC-AUTH-005) |
| TC-AUTH-017 | JSON con sintaxis inválida | 🟡 Media | N/A | 1. Enviar `POST /auth` con el header de referencia y body `{"username": "admin",` (sin cerrar) | Debería responder `400` y no devolver `token` | ✅ Responde `400` con el texto `Bad Request` | Req: criterio QA (estándar HTTP), validar con PO |
| TC-AUTH-018 | Credenciales con tipo número | 🟢 Baja | N/A | 1. Enviar `POST /auth` con el header de referencia y body `{"username": 123, "password": 456}` | Debería responder `400` y no devolver `token` | ❌ Responde `200` con `{"reason": "Bad credentials"}`; no devuelve `token` | Req: tipo texto según la documentación; código: criterio QA, validar con PO<br>Bug: pendiente (mismo que TC-AUTH-005) |
| TC-AUTH-019 | Método `GET` en vez de `POST` | 🟢 Baja | N/A | 1. Enviar `GET /auth` sin body | A confirmar | 🔍 Responde `404` con el texto `Not Found` | Comportamiento actual: `404`<br>A confirmar: ¿`404` o `405 Method Not Allowed`? |

## Resumen

- **Total:** 19 casos. 🔴 4 · 🟡 9 · 🟢 6.
- **Estados:** ✅ 4 · ❌ 11 · 🔍 4 · ⏸ 0 · sin ejecutar 0.
- **A confirmar:** 4.
- Los 11 ❌ son **un solo bug**: la API responde `200` ante cualquier error de login o de formato. En ningún caso devuelve un token indebido.

## Orden de ejecución sugerido

1. 🔴 TC-AUTH-001, TC-AUTH-002, TC-AUTH-005, TC-AUTH-006
2. 🟡 TC-AUTH-007, TC-AUTH-008, TC-AUTH-009, TC-AUTH-010, TC-AUTH-013, TC-AUTH-014, TC-AUTH-015, TC-AUTH-016, TC-AUTH-017
3. 🟢 TC-AUTH-003, TC-AUTH-004, TC-AUTH-011, TC-AUTH-012, TC-AUTH-018, TC-AUTH-019

## Preguntas para el PO

1. La documentación no define las respuestas de error. ¿Confirmas `401` para credenciales incorrectas, `400` para petición mal formada y `415` sin `Content-Type`? (TC-AUTH-005 a 010, 013 a 018)
2. ¿Cada petición debe generar un token nuevo? ¿El anterior sigue valiendo? ¿Cuándo caduca? (TC-AUTH-004)
3. ¿`ADMIN` y `admin` deben ser el mismo usuario? (TC-AUTH-011)
4. ¿Deben ignorarse los espacios delante y detrás del usuario? (TC-AUTH-012)
5. ¿`GET /auth` debe responder `404` o `405`? (TC-AUTH-019)

## Fuera de alcance

- Caducidad del token: no está documentada (ver pregunta 2).
- Bloqueo tras muchos intentos fallidos (fuerza bruta): es un servicio público compartido y no se debe atacar.
- Rendimiento: no hay requisito. Tiempo observado entre 0,34 s y 0,52 s por petición.
- Otros usuarios: la documentación solo publica `admin`.

## Registro de ejecuciones

| Fecha | Entorno | Navegador | Usuario | Quién | Casos | Observaciones |
|---|---|---|---|---|---|---|
| 22/10/2026 | restful-booker.herokuapp.com | N/A (API, `curl`) | admin | Claude | TC-AUTH-001 a 019 | Ejecutado con `curl`, no con REST Client. Reserva propia de TC-AUTH-002 (id `454`) borrada al terminar |
