#!/usr/bin/env bash
set -euo pipefail
until mysqladmin ping -h "$MOODLE_DB_HOST" -u moodle -pmoodle --silent; do sleep 2; done
if ! php admin/cli/cfg.php --name=version >/dev/null 2>&1; then
  php admin/cli/install_database.php --agree-license --adminuser=admin \
    --adminpass='LocalOnly-ChangeMe1!' --adminemail=admin@example.invalid \
    --fullname='Course Package Lab' --shortname='CourseLab'
fi
exec "$@"
