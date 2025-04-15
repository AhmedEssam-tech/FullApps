from odoo import api, fields, models

class BookingAccommodation(models.Model):
    _name="booking_accommodation"
    _Description ="Booking Accommodation"

    tour_reservation = fields.Many2one("tour_booking", string="Tour Reservation", required=1)
    name = fields.Many2one('accommodation', string="Hotel Name", required=1)
    date_in = fields.Datetime(string="Date In ")
    date_out = fields.Datetime(string="Date Out ")
    other_detail = fields.Text()
    room_type = fields.Many2one("room_type", string="Room Type", required=1)
    number_of_pax=fields.Integer()
    meal = fields.Many2one('meal', string='Meal')
    booked_by = fields.Many2one(related="tour_reservation.booking_id", string='Booked By', required=1)
    cost_price = fields.Integer()
    sale_price = fields.Integer()
    tour_name = fields.Many2one("tour", string="Tour Name", required=1)
    tour_start_date = fields.Date(related="tour_name.tour_details_ids.start_date", string="Tour Start Date")
    cost_ids = fields.One2many("cost", "cost_book_id", string="Cost")
