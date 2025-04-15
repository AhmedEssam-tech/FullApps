from odoo import api, fields, models


# _______________add place_______________________________________
class Place(models.Model):
    _name = "place"

    name = fields.Char(string='Name' ,required="1")


# _______________add transport_______________________________________
class TransportType(models.Model):
    _name = "transport"

    name = fields.Char(string='Transport Type', required="1")


# _______________add travel class_______________________________________
class TravelClass(models.Model):
    _name = "travel_class"

    name = fields.Char(string='Travel Class' ,required="1")



# _____________ tour Detail _______________________________________

class TourDetail(models.Model):
    _name = "tour_details"

    tour_details_id = fields.Many2one('tour')
    name = fields.Char(string='Tour Season', required="1")
    start_date=fields.Date("Start Date")
    last_date=fields.Date("Last Date Of Booking")
    payment_date=fields.Date("Payment Due Date")
    total_seat=fields.Integer("Total Seat")
    available_seat=fields.Integer("Available Seat")
    status = fields.Selection([("avl", "Available"),
                              ("confirm", "Confirm"),
                              ("closed", "Closed"),
                              ("cancel", "Cancelled")], required="1", string="Status")




 # _____________ travel information _______________________________________
    class TravelInformation(models.Model):
        _name = "travel_information"

        travel_info_id = fields.Many2one('tour')
        from_tour = fields.Many2one("place",string='From',required="1")
        to_tour = fields.Many2one("place",string='TO',required="1")
        transport_type = fields.Many2one("transport",string='Transport Type')
        travel_class = fields.Many2one("travel_class",string='Travel Class')
        distance = fields.Integer(string='Distance in KM')
        duration_time = fields.Integer(string='Duration Time(hrs)')


# _____________________payment policy ____________________________________
class PaymentPolicy(models.Model):
    _name = "payment_policy"
    _Description = "payment policy"

    name = fields.Char(string='Payment Policy')


# _____________________flight_name ____________________________________
class FlightName(models.Model):
    _name = "flight_name"
    _Description = "flight_name"

    name = fields.Char(string='Name')


# _____________________Accommodation ____________________________________
class Accommodation(models.Model):
    _name = "accommodation"
    _Description = "Accommodation Information"

    name = fields.Char()
    phone = fields.Char()
    room_type = fields.Char(string="Room Type")
    email = fields.Char()
    accommodation_info_ids = fields.One2many('accommodation_information', 'accommodation_info_id')


# _____________________Accommodation information  ____________________________________
class AccommodationInformation(models.Model):
    _name = "accommodation_information"
    _Description = "Accommodation Information "

    accommodation_info_id=fields.Many2one('accommodation')
    room_type = fields.Char(string="room type" ,required="1")
    cost_price = fields.Integer()
    sale_price = fields.Integer()
    description = fields.Char()


# _______________visa Documentation list_______________________________________
class VisaDocumentationList(models.Model):
    _name = "visa_documentation_list"
    _Description = "Visa Documentation List"

    name = fields.Char(string='Name' ,required="1")




# _______________Room Type_______________________________________
class RoomType(models.Model):
     _name = "room_type"
     _Description = "Room Type"

     name = fields.Char(string='Name' ,required="1")



# _______________meal_______________________________________
class Meal(models.Model):
    _name = "meal"

    name = fields.Char(string='Name' ,required="1")


