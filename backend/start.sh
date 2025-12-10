#!/bin/bash
# Start script for Railways deployment
# Handles PORT environment variable expansion

PORT=${PORT:-8000}
exec uvicorn main:app --host 0.0.0.0 --port $PORT

