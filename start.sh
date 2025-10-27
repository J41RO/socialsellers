#!/bin/bash
set -e

echo "🚀 Starting Uvicorn server (WITHOUT Alembic for testing)..."
exec uvicorn app.main_minimal:app --host 0.0.0.0 --port ${PORT:-8000}
