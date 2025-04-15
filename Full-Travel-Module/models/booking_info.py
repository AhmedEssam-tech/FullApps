from odoo import api, fields, models

from email.policy import default


class  BookingInformation(models.Model):
    _name="tour_booking_information"
    _Description ="Tour Booking Information"


    name=fields.Char(default="New" ,readonly=1)
    tour_reservation=fields.Many2one('tour_booking', required=1)
    total_number_of_pax=fields.Integer(required=1)
    booking_date=fields.Date(required=1)
    customer_id=fields.Many2one('res.partner',string='customer' ,required=1)
    email = fields.Char(related="customer_id.email", string='Email')
    mobile = fields.Char(related="customer_id.mobile", string='Mobile Number')
    adult = fields.Integer(string='Adult')
    child = fields.Integer(string='Child')
    infant=fields.Integer(string='Infant')


    # _____________________tour information_______________
    tour_id=fields.Many2one('tour',string='Tour' ,required=1)
    tour_type = fields.Char(related="tour_id.tour_type", string='Tour Type')
    remarks=fields.Text(string='Remarks')
    tour_start_date=fields.Date(string='Tour Start Date')
    tour_season = fields.Selection([("summer", "Summer"),
                               ("autumn", "Autumn"),
                               ("winter", "Winter"),
                               ("spring", "Spring")],  string="Tour Season")
    payment_policy=fields.Many2one('payment_policy',string='Payment Policy' ,required=1)
    person_info_ids=fields.One2many('person_information','persona_info_id')





    @api.model
    def create(self, vals):
        res = super(BookingInformation, self).create(vals)
        if res.name == "New":
            res.name = self.env["ir.sequence"].next_by_code("booking_info")
        return res




    # ____________________person information_______________________
class PersonInformation(models.Model):
    _name = "person_information"
    _Description = "Person Information"

    persona_info_id=fields.Many2one('tour_booking_information')
    name=fields.Many2one('res.partner',string='Name' ,required=1)
    gender=fields.Selection([("male", "Male"),
                               ("female", "Female")],  string="Gander")
    person_type=fields.Selection([("adult", "Adult"),
                               ("child", "Child"),
                               ("infant", "Infant")],  string="Person Type")
