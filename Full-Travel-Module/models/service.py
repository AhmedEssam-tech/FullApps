from odoo import api, fields, models

class  Service(models.Model):
    _name="service"
    _Description ="Service"

    name=fields.Char(string="service name",required=1)
    datetime=fields.Date(string="Datetime")
    number_of_pax=fields.Integer()
    passenger_names=fields.Many2many('res.partner')
    from_tour=fields.Many2one("place",string="From",required=1)
    to_tour=fields.Many2one("place",string="to",required=1)
    driver=fields.Many2one('res.partner',string='Driver' )
    guide=fields.Many2one('res.partner',string='Guide' )
    service_remarks=fields.Text()
    cost_ids=fields.One2many("cost","cost_id",string="Cost")
    tour_reservation=fields.Many2one("tour_booking",string="Tour Reservation",required=1)



# _____________________extra service___________________________
class  ExtraService(models.Model):
    _name="extra_service"
    _Description ="Extra_Service "
    _inherits = {'service': 'service_id'}

    service_id = fields.Many2one('service')
    agent = fields.Many2one('res.partner', string='Agent')
    sub_agent = fields.Many2one('res.partner', string='Sub Agent')
    tour_consultant=fields.Many2one('res.partner', string='Tour Consultant')
    currency=fields.Many2one('res.currency', string='Currency')




# _____________________cost___________________________
class  Cost(models.Model):
    _name="cost"
    _Description ="Cost"

    name = fields.Selection([("adult", "Adult"),
                                    ("child", "Child"),
                                    ("infant", "Infant")], string="Person Type")
    number_of_pax = fields.Integer()
    cost = fields.Integer()
    cost_id = fields.Many2one('service')
    cost_book_id = fields.Many2one('booking_accommodation')

