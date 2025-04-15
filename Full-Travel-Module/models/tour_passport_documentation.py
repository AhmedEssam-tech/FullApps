from odoo import api, fields, models

class TourPassportDocumentation(models.Model):
    _name="tour_documentation"
    _Description ="Tour Passport Documentation"

    name = fields.Char(default="New", readonly=1)
    customer_name_id = fields.Many2one('res.partner', string='Customer Name', required=1)
    Create_date = fields.Date(string="Create Date ")
    mobile = fields.Char(related="customer_name_id.mobile", string='Mobile')
    email = fields.Char(related="customer_name_id.email", string='Email')
    tour= fields.Many2one("tour", string="Tour ", required=1)
    service = fields.Many2one('service', string='Service')
    service_scheme = fields.Char(string='Service Scheme')
    service_cost = fields.Integer( string='Service Cost')
    tour_Passport_ids = fields.One2many("visa_documentation", "tour_Passport_id")
    status = fields.Selection([("draft", "Draft"),
                               ("approval", "In progress/Approval"),
                               ("confirmed", "Confirmed"),
                               ("done", "Done"),
                               ("cancel", "Cancel"), ], string="Status", default="draft")
    invoice_count = fields.Integer(string="Number of Invoices", compute='_compute_invoice_count')



    @api.depends('customer_name_id')
    def _compute_invoice_count(self):
        for record in self:
            record.invoice_count = self.env['account.move'].search_count([('partner_id', '=', record.id), ('move_type', '=', 'out_invoice')])

    def action_view_invoices(self):
        return {
            'name': 'Invoices',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('partner_id', '=', self.id), ('move_type', '=', 'out_invoice')],
            'context': dict(self._context, create=False),
        }



    def action_approval(self):
        for res in self:
            res.status = 'approval'

    def action_confirmed(self):
        for res in self:
            res.status = 'confirmed'

    def action_done(self):
        for res in self:
            res.status = 'done'

    def action_cancel(self):
        for res in self:
            res.status = 'cancel'

    def action_invoice(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('move_type', '=', 'out_invoice')],
            'target': 'current',
        }

    @api.model
    def create(self, vals):
        res = super(TourPassportDocumentation, self).create(vals)
        if res.name == "New":
            res.name = self.env["ir.sequence"].next_by_code("passport_documentation_seq")
        return res
