#!/bin/bash
set -e

# Substitute environment variables into odoo.conf
sed -e "s|__DB_HOST__|${DB_HOST:-db}|g" \
    -e "s|__DB_PORT__|${DB_PORT:-5432}|g" \
    -e "s|__DB_USER__|${DB_USER:-odoo}|g" \
    -e "s|__DB_PASSWORD__|${DB_PASSWORD:-odoo}|g" \
    -e "s|__DB_NAME__|${DB_NAME:-postgres}|g" \
    -e "s|__ADMIN_PASSWD__|${ADMIN_PASSWD:-orphan-admin-strong-passwd}|g" \
    /etc/odoo/odoo.conf.template > /etc/odoo/odoo.conf

# Remove the old odoo.conf if it exists (we use the template now)
rm -f /etc/odoo/odoo.conf.bak 2>/dev/null || true

exec "$@"
