from odoo import api, fields, models

class TourReservation(models.Model):
    _name="tour"
    _Description="tour reservation"


    name=fields.Char(required=1 ,string='Tour Name')
    tour_type = fields.Char(string='Tour Type')
    tour_days = fields.Integer(string='Tour Days')
    tour_code = fields.Char(default="0", readonly=1,string='Tour Code')
    date_of_publish = fields.Date(string="Date of Publish")
    tour_plans = fields.Char(required=1, string='Tour Plans')
    travel_info_ids = fields.One2many("travel_information","travel_info_id" )
    tour_details_ids = fields.One2many("tour_details","tour_details_id" )
    status = fields.Selection([("draft", "Draft"),
                             ("confirmed", "Confirmed")],string="Status",default="draft")


    def action_confirm(self):
        for res in self:
            res.status='confirmed'



    @api.model
    def create(self, vals):
        res = super(TourReservation, self).create(vals)
        if res.tour_code == "0":
            res.tour_code = self.env["ir.sequence"].next_by_code("tour_program_code")
        return res