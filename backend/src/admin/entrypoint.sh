#!/bin/sh

set -e

ADMIN_PASSWORD_PATH="/run/secrets/admin_password"

if [ ! -f "$ADMIN_PASSWORD_PATH" ] || [ ! -s "$ADMIN_PASSWORD_PATH" ]; then
  echo "Error: Required secret admin_password is missing or empty."
  exit 1
fi

cd cli

python migrations.py migrate;

user_count=$(python users.py list | wc -l);

# If no users have been created create a new one with a random password
if [ "$user_count" -eq 0 ]; then
  username=$(tr -dc 'A-Za-z' < /dev/urandom | head -c 13; echo);
  email="contact@vectorinterior.design";
  password=$(tr -dc 'A-Za-z0-9!#$%&\()*+,-./:;<=>?@[\]^_{|}~' </dev/urandom | head -c 13; echo);

  python users.py new -n "$username" -e "$email" -p "$password";

  echo "Default user created successfully. Name: $username Email: $email password: $password";
fi

cd ..

if [ $DEV_MODE = 1 ]; then
    sanic app:create_app --host=0.0.0.0 --port=80 --factory --dev
else
    sanic app:create_app --host=0.0.0.0 --port=80 --factory
fi
