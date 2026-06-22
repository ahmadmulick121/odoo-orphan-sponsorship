from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    brevo_api_key = fields.Char(
        string='Brevo API Key',
        config_parameter='orphan_brevo_mail.api_key',
        help='API key from Brevo dashboard (xkeysib-...)')
    brevo_sender_email = fields.Char(
        string='Brevo Sender Email',
        config_parameter='orphan_brevo_mail.sender_email',
        help='From-address for outgoing mail (must be a verified sender in Brevo)')
    brevo_sender_name = fields.Char(
        string='Brevo Sender Name',
        config_parameter='orphan_brevo_mail.sender_name',
        default='Orphan Sponsorship')
