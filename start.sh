#!/bin/bash
set -e

echo "🔍 DEBUG: PORT variable = ${PORT}"
echo "🔍 DEBUG: Will bind to port ${PORT:-8000}"
echo "🔍 DEBUG: Current directory = $(pwd)"
echo "🔍 DEBUG: Python version = $(python --version)"
echo "🔍 DEBUG: Testing if app can be imported..."
python -c "from app.main_minimal import app; print('✅ Import successful')"

echo "🚀 Starting Uvicorn server on 0.0.0.0:${PORT:-8000}..."
echo "🔍 DEBUG: Uvicorn will log ALL requests with --access-log"
exec uvicorn app.main_minimal:app \
  --host 0.0.0.0 \
  --port ${PORT:-8000} \
  --log-level debug \
  --access-log
