FROM odoo:16.0

USER root

# Copy custom modules
COPY orphan_sponsorship/ /mnt/extra-addons/orphan_sponsorship/
COPY orphan_brevo_mail/ /mnt/extra-addons/orphan_brevo_mail/

# Copy odoo config template + entrypoint
COPY config/odoo.conf.template /etc/odoo/odoo.conf.template
COPY config/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh
RUN chown -R odoo:odoo /mnt/extra-addons /etc/odoo

USER odoo

EXPOSE 8069

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["odoo", "--config=/etc/odoo/odoo.conf"]
