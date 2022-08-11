#!/usr/bin/env sh

echo "Starting app..."
alembic upgrade head;
uvicorn app.main:app --host "0.0.0.0" --port "3000";
