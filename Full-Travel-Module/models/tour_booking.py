from odoo import api, fields, models

class TourBooking(models.Model):
    _name="tour_booking"
    _Description ="Tour Booking"

    name = fields.Char(default="New", readonly=1 ,string="Booking/File Number")
    agent_file = fields.Char(string="Agent/File Number")
    agent = fields.Many2one('res.partner', string='Agent')
    sub_agent = fields.Many2one('res.partner', string='Sub Agent')
    booking_date = fields.Date(required=1)
    booking_id = fields.Many2one('res.partner', string='Booking Name', required=1)
    currency = fields.Many2one('res.currency', string='Currency')
    status = fields.Selection([("draft", "Draft"),
                               ("approval", "In progress/Approval"),
                               ("confirmed", "Confirmed")], string="Status")

    @api.model
    def create(self, vals):
        res = super(TourBooking, self).create(vals)
        if res.name == "New":
            res.name = self.env["ir.sequence"].next_by_code("tour_booking_seq")
        return res