#!/bin/bash

set -e

USER_PASSWORD_PATH="/run/secrets/user_password"


if [ ! -f "$USER_PASSWORD_PATH" ] || [ ! -s "$USER_PASSWORD_PATH" ]; then
  echo "Error: Required secret user_password is missing or empty."
  exit 1
fi

runningPort=$PORT

if [ "$BUILD_TARGET" == "dev" ]; then
    sanic app:create_app --host=0.0.0.0 --port=$runningPort --factory --debug
else
    sanic app:create_app --host=0.0.0.0 --port=$runningPort --factory
fi
