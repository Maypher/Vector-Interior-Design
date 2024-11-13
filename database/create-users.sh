#!/bin/bash

function genPassword {
    openssl rand -base64 $1;
}

rootPassword=$(genPassword 12);

adminName="adminBackend";
adminPassword=$(genPassword 12);

userName="userBackend";
userPassword=$(genPassword 12);

export PGPASSWORD="$POSTGRES_PASSWORD"

psql -U postgres << EOF
BEGIN;
CREATE USER $adminName WITH PASSWORD '$adminPassword';

CREATE USER $userName WITH PASSWORD '$userPassword';
COMMIT;
EOF

echo "Usuario $adminName creado con contraseña: $adminPassword";
echo "Usuario $userName reado con contraseña: $userPassword";
