#!/bin/bash

set -e

# Trap errors and print the error message
trap 'echo "Error on line $LINENO: $BASH_COMMAND"' ERR

ADMIN_PASSWORD_PATH="/run/secrets/admin_password"

if [ ! -f "$ADMIN_PASSWORD_PATH" ] || [ ! -s "$ADMIN_PASSWORD_PATH" ]; then
  echo "Error: Required secret admin_password is missing or empty."
  exit 1
fi

USER_PASSWORD_PATH="/run/secrets/user_password"

if [ ! -f "$USER_PASSWORD_PATH" ] || [ ! -s "$USER_PASSWORD_PATH" ]; then
  echo "Error: Required secret user_password is missing or empty."
  exit 1
fi

ADMIN_PASSWORD=$(tr -d '\r' </run/secrets/admin_password);
USER_PASSWORD=$(tr -d '\r' </run/secrets/user_password);

psql -U postgres << EOF
BEGIN;

CREATE USER $ADMIN_USERNAME WITH PASSWORD '$ADMIN_PASSWORD';
CREATE USER $USER_USERNAME WITH PASSWORD '$USER_PASSWORD';

GRANT CREATE ON SCHEMA public TO $ADMIN_USERNAME;
GRANT CREATE ON DATABASE postgres TO $ADMIN_USERNAME;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO $ADMIN_USERNAME;
ALTER DEFAULT PRIVILEGES FOR ROLE $ADMIN_USERNAME IN SCHEMA public GRANT SELECT ON TABLES TO $USER_USERNAME;

CREATE SCHEMA IF NOT EXISTS administration AUTHORIZATION $ADMIN_USERNAME;

COMMIT;
EOF
