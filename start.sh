#!/bin/bash

echo "🔄 Running database migrations..."
if alembic upgrade head; then
    echo "✅ Migrations completed successfully"
else
    echo "⚠️  WARNING: Migrations failed, but continuing anyway..."
fi

echo "🚀 Starting Uvicorn server..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
