#!/bin/bash

set -e

ADMIN_PASSWORD_PATH="/run/secrets/admin_password"

if [ ! -f "$ADMIN_PASSWORD_PATH" ] || [ ! -s "$ADMIN_PASSWORD_PATH" ]; then
  echo "Error: Required secret admin_password is missing or empty."
  exit 1
fi

runningPort=$PORT

if [ "$BUILD_TARGET" = 'dev' ]; then
    sanic app:create_app --host=0.0.0.0 --port=$runningPort --factory --dev
else
    sanic app:create_app --host=0.0.0.0 --port=$runningPort --factory
fi
