from odoo import api, fields, models



class  DaySheet(models.Model):
    _name="day_sheet"
    _Description ="Day Sheet"

    name = fields.Char(default="New", readonly=1,string='File Number')
    service_date = fields.Date(required=1)
    extra_service_date = fields.Date(required=1)
    booking_name = fields.Many2one('res.partner', string='Booking Name')
    booking_date = fields.Date(required=1)
    agent = fields.Many2one('res.partner', string='Agent')
    driver = fields.Many2one('res.partner', string='Driver')
    guide = fields.Many2one('res.partner', string='Guide')



