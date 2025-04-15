from odoo import api, fields, models

class TourItinerary(models.Model):
    _name="tour_itinerary"
    _Description="Tour Itinerary"

    name = fields.Char(default="New", readonly=1)
    customer_inquiry_id = fields.Many2one('tour_inquiry', string='Customer Inquiry',required=1)
    address = fields.Char(related="customer_inquiry_id.address", string='Address')
    street = fields.Char(related="customer_inquiry_id.street", string='Address')
    tour_id = fields.Many2one('tour', string='Tour', required=1)
    partner_id = fields.Many2one(related="customer_inquiry_id.partner_id", string='Lead BY', required=1)
    contact = fields.Many2one(related="customer_inquiry_id.contact", string='Contact Name')
    email = fields.Char(related="customer_inquiry_id.email", string='Email')
    reference = fields.Char(related="customer_inquiry_id.reference",string='Reference')
    tour_program_ids = fields.One2many('tour_program', 'tour_program_id')


    # ________________________ Tour information ________________________
    start_date_p = fields.Date(related="customer_inquiry_id.start_date",string="Prefer start Date")
    end_date = fields.Date(related="customer_inquiry_id.end_date",string="Prefer End Date")
    room_required=fields.Integer(string="Room Required")
    adult = fields.Integer(related="customer_inquiry_id.number_of_adult", string="Adult")
    child = fields.Integer(related="customer_inquiry_id.number_of_child", string="Child")
    currency=fields.Many2one('res.currency', string='Currency')
    payment_policy = fields.Many2one('payment_policy', string='Payment Policy' ,required=1)


    # _____________________Tour  date details____________________________________
    start_date = fields.Date(related="tour_id.tour_details_ids.start_date",string="Start Date")
    booking_last_date = fields.Date(related="tour_id.tour_details_ids.last_date",string="Booking last Date")
    payment_due_date = fields.Date(related="tour_id.tour_details_ids.payment_date",string="Payment Due Date")
    total_seats = fields.Integer(related="tour_id.tour_details_ids.total_seat",string='Total Seats')

    @api.model
    def create(self, vals):
        res = super(TourItinerary, self).create(vals)
        if res.name == "New":
            res.name = self.env["ir.sequence"].next_by_code("tour_itinerary_seq")
        return res



# __________tour program_______________
class TourProgram(models.Model):
    _name="tour_program"
    _Description="Tour program"

    tour_program_id = fields.Many2one('tour_itinerary', required=1)
    tour_id = fields.Many2one(related="tour_program_id.tour_id", string='Tour', required=1)
    tour_code=fields.Char(related="tour_program_id.tour_id.tour_code",string="Code")
    tour_days=fields.Integer(related="tour_id.tour_days",string='Tour Days')
    tour_nights=fields.Integer(string='Tour Nights')
    tour_day_des=fields.Text(string='Tour Day Description')
    breakfast=fields.Boolean()
    lunch=fields.Boolean()
    dinner=fields.Boolean()

