from odoo import models, fields


class OrphanSponsorshipDonor(models.Model):
    _name = 'orphan.sponsorship.donor'
    _description = 'Donor'
    _inherit = ['mail.thread']
    _order = 'create_date asc'

    name = fields.Char(string='Full Name', required=True, tracking=True)
    email = fields.Char(string='Email', required=True, tracking=True)
    phone = fields.Char(string='Phone')
    state = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string='Status', default='active', tracking=True)
    orphan_ids = fields.One2many('orphan.sponsorship.orphan', 'donor_id', string='Sponsored Orphans')
    orphan_count = fields.Integer(compute='_compute_orphan_count', string='Orphans')

    def _compute_orphan_count(self):
        for rec in self:
            rec.orphan_count = len(rec.orphan_ids)
