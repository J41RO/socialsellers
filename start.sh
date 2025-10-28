#!/bin/bash
# Script de inicio para Railway
# Expande correctamente la variable PORT

PORT=${PORT:-8080}
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
