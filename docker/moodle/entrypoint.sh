#!/usr/bin/env bash
set -euo pipefail
until mysqladmin ping -h "$MOODLE_DB_HOST" -u moodle -pmoodle --silent; do sleep 2; done

# Decide install-vs-skip by looking for a Moodle table directly, rather than
# booting Moodle with admin/cli/cfg.php: that bootstrap races a fresh
# moodledata volume and, when it flakes, install_database.php then aborts on the
# seeded database with "Database tables already present".
installed=$(mysql -h "$MOODLE_DB_HOST" -u moodle -pmoodle -N -B \
  -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = 'mdl_config'" \
  moodle 2>/dev/null || echo 0)

if [ "${installed:-0}" = "0" ]; then
  # Fresh database: install Moodle. This also creates the admin account with the
  # local-only password below.
  php admin/cli/install_database.php --agree-license --adminuser=admin \
    --adminpass='Local-Admin-2026' --adminemail=admin@example.invalid \
    --fullname='Course Package Lab' --shortname='CourseLab'
else
  # The database is already populated (a reused volume or the docker/mariadb-seed
  # snapshot, which is built from the current Moodle code and already carries the
  # local-only admin password). Clear the regenerable cache/lock trees on the
  # filesystem: this is equivalent to purge_caches but cannot wedge on a Moodle
  # bootstrap cache lock the way any CLI script (purge_caches.php, upgrade.php,
  # reset_password.php) can on a fresh moodledata volume. Then apply a real
  # pending schema upgrade only, time-boxed so a wedged bootstrap cannot block
  # startup - re-run bin/build-moodle-seed after bumping the Moodle version so
  # this stays a fast no-op.
  rm -rf /var/www/moodledata/cache/* /var/www/moodledata/localcache/* \
         /var/www/moodledata/lock/* /var/www/moodledata/muc/* 2>/dev/null || true
  timeout 150 php admin/cli/upgrade.php --non-interactive >/dev/null 2>&1 || true
  rm -rf /var/www/moodledata/cache/* /var/www/moodledata/lock/* \
         /var/www/moodledata/muc/* 2>/dev/null || true
fi

exec "$@"
