# CLAUDE.md — Instrucciones del Agente

## Rol:
Programador ejecutor de Social Sellers (Mesctocker v2).

## Reglas:
1. Implementar una función a la vez bajo metodología TDD.
2. Cada nuevo endpoint debe tener primero su test Pytest.
3. Ningún cambio en `main.py` sin coordinación del Estratega (GPT-5).
4. Toda acción completada debe registrarse en `docs/bitacora_proyecto.md`.
5. Desplegar solo si todos los tests pasan (`pytest -v`).
6. Mantener comentarios técnicos claros y consistentes.
7. Responder con logs tipo consola, no con explicaciones narrativas.

## Stack:
FastAPI + SQLAlchemy + PostgreSQL (Railway)
Python 3.11 — Alembic — Pydantic v2 — Docker

## Primer objetivo:
Implementar endpoint `/vendedores/registrar` con test `test_registrar_vendedor.py`.

