FROM odoo:16.0

USER root

# Copy custom modules
COPY orphan_sponsorship/ /mnt/extra-addons/orphan_sponsorship/
COPY orphan_brevo_mail/ /mnt/extra-addons/orphan_brevo_mail/

# Copy odoo config template + entrypoint
COPY config/odoo.conf.template /etc/odoo/odoo.conf.template
COPY config/entrypoint.sh /usr/local/bin/orphan-entrypoint.sh

# Fix line endings (in case uploaded from Windows via web UI), make executable
RUN sed -i 's/\r$//' /usr/local/bin/orphan-entrypoint.sh && \
    chmod +x /usr/local/bin/orphan-entrypoint.sh && \
    chown -R odoo:odoo /mnt/extra-addons /etc/odoo

USER odoo

EXPOSE 8069

# Override the base image entrypoint completely
ENTRYPOINT ["/usr/local/bin/orphan-entrypoint.sh"]
CMD ["odoo"]
