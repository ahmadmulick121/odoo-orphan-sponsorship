#!/bin/bash
set -e

echo "===== Orphan Sponsorship entrypoint starting ====="
echo "DB_HOST=${DB_HOST}"
echo "DB_PORT=${DB_PORT}"
echo "DB_USER=${DB_USER}"
echo "DB_NAME=${DB_NAME}"

# Generate odoo.conf from template
sed -e "s|__DB_HOST__|${DB_HOST:-localhost}|g" \
    -e "s|__DB_PORT__|${DB_PORT:-5432}|g" \
    -e "s|__DB_USER__|${DB_USER:-odoo}|g" \
    -e "s|__DB_PASSWORD__|${DB_PASSWORD:-odoo}|g" \
    -e "s|__DB_NAME__|${DB_NAME:-postgres}|g" \
    -e "s|__ADMIN_PASSWD__|${ADMIN_PASSWD:-admin}|g" \
    /etc/odoo/odoo.conf.template > /etc/odoo/odoo.conf

echo "===== Generated odoo.conf ====="
grep -E "^(db_|http_|admin_)" /etc/odoo/odoo.conf
echo "==============================="

# Run odoo with our generated config
exec odoo --config=/etc/odoo/odoo.conf "$@"
