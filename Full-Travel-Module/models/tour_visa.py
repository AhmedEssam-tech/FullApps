from odoo import api, fields, models

class TourVisa1(models.Model):
    _name="tour_visa"
    _Description ="Tour Visa"

    name = fields.Char(default="New", readonly=1,string="Name", required=1)
    customer_name = fields.Many2one('res.partner', string='Customer Name')
    mobile = fields.Char(related="customer_name.mobile", string='Mobile')
    email = fields.Char(related="customer_name.email", string='Email')
    visa=fields.Char(string='Visa')
    service_cost = fields.Integer(string="Service Cost")
    tour_date = fields.Date(string="Tour Date")
    return_date = fields.Date(string="Return Date")
    tour_id = fields.Many2one('tour', string='Tour', required=1)
    # tour_booking_ref = fields.Many2one('tour_booking', string='Tour Booking Ref')
    tour_booking = fields.Many2one('tour_booking', string='Tour Booking Ref')
    service = fields.Many2one('service', string='Service')
    visa_ids = fields.One2many("visa_documentation", "visa_id")
    status = fields.Selection([("draft", "Draft"),
                               ("approval", "In progress/Approval"),
                               ("confirmed", "Confirmed"),
                               ("done", "Done"),
                               ("cancel", "Cancel"),], string="Status",default="draft")







    def action_approval(self):
        for res in self:
            res.status='approval'


    def action_confirmed(self):
        for res in self:
            res.status='confirmed'


    def action_done(self):
        for res in self:
            res.status='done'

    def action_cancel(self):
        for res in self:
            res.status='cancel'


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
        res = super(TourVisa1, self).create(vals)
        if res.name == "New":
            res.name = self.env["ir.sequence"].next_by_code("tour_visa_seq")
        return res




# ___________________Visa Documentation_______________________________
class VisaDocumentation(models.Model):
    _name="visa_documentation"
    _Description ="Visa Documentation"

    name = fields.Many2many('visa_documentation_list', string='Documentation Name')
    attachment_ids = fields.Many2many('ir.attachment',string='Attachments')
    expiry_date = fields.Date(string="Expiry Date")
    visa_id = fields.Many2one('tour_visa')
    tour_Passport_id = fields.Many2one('tour_documentation')
