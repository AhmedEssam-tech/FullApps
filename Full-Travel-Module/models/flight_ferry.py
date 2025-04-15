from odoo import api, fields, models

class Flight(models.Model):
    _name="flight"
    _Description ="Flight"


    name=fields.Many2one('flight_name',string="Flight Name" ,required=1)
    date_in=fields.Datetime(string="Date in and time")
    date_out=fields.Datetime(string="Date out and time")
    from_tour = fields.Many2one("place", string="From", required=1)
    to_tour = fields.Many2one("place", string="to", required=1)
    booked_by = fields.Many2one('res.partner', string='Booked By', required=1)
    other_detail=fields.Text()
    tour_reservation = fields.Many2one("tour_booking", string="Tour Reservation", required=1)
    cost = fields.Integer()
    cost_ids = fields.One2many("cost", "cost_id", string="Cost")



      # _____________________ferry___________________________
class Ferry(models.Model):
    _name="ferry"
    _Description ="Ferry "
    _inherits = {'flight': 'flight_id'}


    flight_id=fields.Many2one("flight")
    name = fields.Char(string="Flight Name" ,required=1)

