from odoo import models, fields, api


class OrphanSponsorshipOrphan(models.Model):
    _name = 'orphan.sponsorship.orphan'
    _description = 'Orphan'
    _inherit = ['mail.thread']
    _order = 'create_date asc'

    name = fields.Char(string='Full Name', required=True, tracking=True)
    age = fields.Integer(string='Age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender', tracking=True)
    location = fields.Char(string='Location', tracking=True)
    status = fields.Selection([
        ('unassigned', 'Unassigned'),
        ('sponsored', 'Sponsored'),
    ], string='Status', default='unassigned', tracking=True)
    donor_id = fields.Many2one('orphan.sponsorship.donor', string='Sponsor', tracking=True)

    @api.model
    def assign_fifo(self):
        """Match unassigned orphans to free active donors, oldest first."""
        unassigned = self.search([('status', '=', 'unassigned')], order='create_date asc')
        assigned_donor_ids = self.search([('status', '=', 'sponsored')]).mapped('donor_id').ids
        free_donors = self.env['orphan.sponsorship.donor'].search([
            ('state', '=', 'active'),
            ('id', 'not in', assigned_donor_ids),
        ], order='create_date asc')

        template = self.env.ref(
            'orphan_sponsorship.email_template_orphan_assigned',
            raise_if_not_found=False)

        for donor, orphan in zip(free_donors, unassigned):
            orphan.write({'donor_id': donor.id, 'status': 'sponsored'})
            orphan.message_post(
                body='Assignment created: orphan paired with %s (%s)' % (
                    donor.name, donor.email or 'no email'))
            if template and donor.email:
                template.send_mail(orphan.id, force_send=True)
        return True

    @api.model
    def send_assignment_emails(self):
        """Re-send notification emails for all currently sponsored orphans."""
        template = self.env.ref(
            'orphan_sponsorship.email_template_orphan_assigned',
            raise_if_not_found=False)
        if not template:
            return False
        sponsored = self.search([
            ('status', '=', 'sponsored'),
            ('donor_id', '!=', False),
        ])
        for orphan in sponsored:
            if orphan.donor_id.email:
                template.send_mail(orphan.id, force_send=True)
        return True
