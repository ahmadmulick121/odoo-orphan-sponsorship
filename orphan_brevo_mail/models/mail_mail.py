import json
import logging
import urllib.request
import urllib.error
from email.utils import parseaddr, getaddresses

from odoo import models, api

_logger = logging.getLogger(__name__)

BREVO_API_URL = 'https://api.brevo.com/v3/smtp/email'


class MailMail(models.Model):
    _inherit = 'mail.mail'

    def send(self, auto_commit=False, raise_exception=False):
        """Override the public send() entry point. When Brevo API key is set,
        deliver via HTTPS API (bypasses SMTP blocks on Railway/Heroku/etc).
        Falls back to default SMTP path when no API key is configured."""
        ICP = self.env['ir.config_parameter'].sudo()
        api_key = ICP.get_param('orphan_brevo_mail.api_key', '').strip()

        if not api_key:
            _logger.info('Brevo: no API key configured, using default SMTP path')
            return super().send(auto_commit=auto_commit, raise_exception=raise_exception)

        sender_email = ICP.get_param('orphan_brevo_mail.sender_email', '').strip()
        sender_name = ICP.get_param('orphan_brevo_mail.sender_name', 'Orphan Sponsorship').strip()

        _logger.info('Brevo: sending %s mail(s) via HTTPS API', len(self))

        for mail in self:
            try:
                self._brevo_send_one(mail, api_key, sender_email, sender_name)
                mail.write({'state': 'sent', 'failure_reason': False})
                _logger.info('Brevo: sent mail id=%s to=%s', mail.id, mail.email_to)
            except Exception as exc:
                _logger.exception('Brevo: failed to send mail id=%s', mail.id)
                mail.write({'state': 'exception',
                            'failure_reason': str(exc)[:1000]})
                if raise_exception:
                    raise
            if auto_commit:
                self.env.cr.commit()
        return True

    def _brevo_send_one(self, mail, api_key, sender_email, sender_name):
        """Build payload for a single mail.mail record and POST it to Brevo."""
        to_list = []
        if mail.email_to:
            for name, addr in getaddresses([mail.email_to]):
                if addr:
                    to_list.append({'email': addr, 'name': name or addr})
        for partner in mail.recipient_ids:
            if partner.email:
                to_list.append({'email': partner.email,
                                'name': partner.name or partner.email})
        if not to_list:
            raise ValueError('No recipient on mail id=%s' % mail.id)

        if not sender_email:
            _name, sender_email = parseaddr(mail.email_from or '')
        if not sender_name:
            sender_name = 'Orphan Sponsorship'
        if not sender_email:
            sender_email = 'noreply@example.com'

        payload = {
            'sender': {'email': sender_email, 'name': sender_name},
            'to': to_list,
            'subject': mail.subject or '(no subject)',
            'htmlContent': mail.body_html or mail.body or '<p></p>',
        }
        if mail.reply_to:
            _n, reply_addr = parseaddr(mail.reply_to)
            if reply_addr:
                payload['replyTo'] = {'email': reply_addr}

        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            BREVO_API_URL,
            data=data,
            method='POST',
            headers={
                'api-key': api_key,
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                body = resp.read().decode('utf-8', 'replace')
                _logger.info('Brevo OK %s: %s', resp.status, body[:300])
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8', 'replace') if e.fp else ''
            _logger.error('Brevo HTTP %s body=%s', e.code, err_body[:500])
            raise RuntimeError('Brevo HTTP %s: %s' % (e.code, err_body[:500])) from e
