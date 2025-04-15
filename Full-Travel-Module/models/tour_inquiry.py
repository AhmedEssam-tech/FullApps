from odoo import api, fields, models

class TourInquiry(models.Model):
    _name="tour_inquiry"
    _Description="tour Inquiry"
    _inherits={'res.partner':'partner_id'}


    name=fields.Char(default="New" ,readonly=1)
    partner_id=fields.Many2one('res.partner',string='Lead BY' ,required=1)
    contact=fields.Many2one('res.partner',string='Contact Name')
    email=fields.Char(related="partner_id.email" ,string='Email')
    mobile=fields.Char(related="partner_id.mobile" ,string='Mobile')
    tour_inquiry_date= fields.Date(string="Tour Inquiry Date")
    address= fields.Char(string='Address')
    number_of_adult=fields.Integer(string='Number Of Adult')
    number_of_child=fields.Integer(string='Number Of Child')
    reference=fields.Char(string='Reference')
    destination_ids=fields.One2many('destination','destination_id')

    # ______________________tour information__________________________
    start_date=fields.Date(string="Prefer start Date")
    budget_min=fields.Integer(string='Budget/person Min')
    budget_max=fields.Integer(string='Budget/person Max')
    notes=fields.Text(string='Notes')
    end_date=fields.Date(string="Prefer End Date")
    confirmed_budget = fields.Integer(string=' Confirmed Budget')



    @api.model
    def create(self,vals):
        res=super(TourInquiry,self).create(vals)
        if res.name=="New":
            res.name=self.env["ir.sequence"].next_by_code("tour_inquiry_seq")
        return res


# ______________________Destination__________________________
class Destination(models.Model):
    _name="destination"

    destination_id=fields.Many2one('tour_inquiry' ,required=1)
    destination = fields.Char(string='Destination')
    country = fields.Many2one('res.country', string='Country')
    location = fields.Many2many('place', string='Location')
    no_of_days = fields.Integer( string='No Of Days')
    no_of_nights = fields.Integer( string='No Of Nights')

