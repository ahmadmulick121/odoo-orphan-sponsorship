from odoo import models, fields


class OrphanSponsorshipDemo(models.Model):
    _name = 'orphan.sponsorship.demo'
    _description = 'Demo Control Panel'

    name = fields.Char(default='Demo Control Panel')

    # ── data ─────────────────────────────────────────────────────────────
    _ORPHANS = [
        {'name': 'Ahmed Ali',      'age': 7,  'gender': 'male',   'location': 'Karachi, Pakistan'},
        {'name': 'Fatima Hassan',  'age': 9,  'gender': 'female', 'location': 'Lahore, Pakistan'},
        {'name': 'Omar Siddiqui',  'age': 6,  'gender': 'male',   'location': 'Islamabad, Pakistan'},
        {'name': 'Aisha Malik',    'age': 8,  'gender': 'female', 'location': 'Peshawar, Pakistan'},
        {'name': 'Yusuf Khan',     'age': 10, 'gender': 'male',   'location': 'Quetta, Pakistan'},
        {'name': 'Zainab Qureshi', 'age': 5,  'gender': 'female', 'location': 'Multan, Pakistan'},
        {'name': 'Hassan Raza',    'age': 11, 'gender': 'male',   'location': 'Faisalabad, Pakistan'},
        {'name': 'Maryam Shah',    'age': 4,  'gender': 'female', 'location': 'Rawalpindi, Pakistan'},
        {'name': 'Ibrahim Javed',  'age': 12, 'gender': 'male',   'location': 'Sialkot, Pakistan'},
        {'name': 'Noor Fatima',    'age': 7,  'gender': 'female', 'location': 'Hyderabad, Pakistan'},
    ]
    _DONORS = [
        {'name': 'Waleed Malik',  'email': 'ahmadmulick121@gmail.com', 'phone': '+1-555-0101'},
        {'name': 'Sara Ahmed',    'email': 'sara@example.com',         'phone': '+1-555-0102'},
        {'name': 'Bilal Khan',    'email': 'bilal@example.com',        'phone': '+1-555-0103'},
        {'name': 'Hina Qureshi',  'email': 'hina@example.com',         'phone': '+1-555-0104'},
        {'name': 'Usman Farooq',  'email': 'usman@example.com',        'phone': '+1-555-0105'},
        {'name': 'Ayesha Raza',   'email': 'ayesha@example.com',       'phone': '+1-555-0106'},
        {'name': 'Tariq Mahmood', 'email': 'tariq@example.com',        'phone': '+1-555-0107'},
        {'name': 'Sana Iqbal',    'email': 'sana@example.com',         'phone': '+1-555-0108'},
        {'name': 'Kamran Ali',    'email': 'kamran@example.com',       'phone': '+1-555-0109'},
        {'name': 'Nadia Sheikh',  'email': 'nadia@example.com',        'phone': '+1-555-0110'},
    ]

    def _notify(self, title, message, kind='success'):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {'title': title, 'message': message, 'type': kind, 'sticky': False}
        }

    # ── buttons ─────────────────────────────────────────────────────────
    def action_load_demo_data(self):
        Orphan = self.env['orphan.sponsorship.orphan']
        Donor = self.env['orphan.sponsorship.donor']
        Orphan.search([]).unlink()
        Donor.search([]).unlink()
        for o in self._ORPHANS:
            Orphan.create({'name': o['name'], 'age': o['age'], 'gender': o['gender'],
                           'location': o['location'], 'status': 'unassigned'})
        for i, d in enumerate(self._DONORS):
            Donor.create({'name': d['name'], 'email': d['email'], 'phone': d['phone'],
                          'state': 'active' if i < 5 else 'inactive'})
        return self._notify(
            'Demo Data Loaded',
            '10 orphans and 10 donors created (5 active, 5 inactive).')

    def action_run_fifo_assignment(self):
        self.env['orphan.sponsorship.orphan'].assign_fifo()
        return self._notify(
            'FIFO Assignment Complete',
            'Eligible orphans paired with active donors. Emails queued.')

    def action_activate_remaining_donors(self):
        inactive = self.env['orphan.sponsorship.donor'].search([('state', '=', 'inactive')])
        n = len(inactive)
        inactive.write({'state': 'active'})
        return self._notify(
            'Donors Activated',
            '%d donors activated. Run FIFO again to assign them.' % n,
            'success')

    def action_reset(self):
        self.env['orphan.sponsorship.orphan'].search([]).write({
            'donor_id': False, 'status': 'unassigned'})
        donors = self.env['orphan.sponsorship.donor'].search([])
        for i, d in enumerate(donors):
            d.state = 'active' if i < 5 else 'inactive'
        return self._notify(
            'Reset Complete',
            'All orphans unassigned. Donors restored to 5 active / 5 inactive.',
            'warning')

    def action_send_emails(self):
        self.env['orphan.sponsorship.orphan'].send_assignment_emails()
        return self._notify(
            'Emails Sent',
            'Assignment notification emails dispatched to all sponsored donors.')
