from odoo import api, fields, models

class Insurance(models.Model):
    _name="insurance"
    _Description ="Insurance"


    name=fields.Char(string="Name" ,required=1)
    adults_cost = fields.Integer(string="Adults cost")
    code = fields.Char(string="Code", size=6)
    childrens_cost = fields.Integer(string="Childrens Cost")



      # _____________________Agent Commission ___________________________
class AgentCommission(models.Model):
    _name="agent_commission"
    _Description ="agent commission "

    name = fields.Char(default="New", readonly=1,string="Name", required=1)
    date = fields.Date(string="Date")
    agent= fields.Many2one('res.partner', string='Agent', required=1)
    price_list = fields.Many2one('res.currency',string="PriceList")
    commission_ids=fields.One2many("commission","commission_id")



    @api.model
    def create(self, vals):
        res = super(AgentCommission, self).create(vals)
        if res.name == "New":
            res.name = self.env["ir.sequence"].next_by_code("agent_commission_seq")
        return res

class Commission(models.Model):
    _name = "commission"
    _Description = "agent commission "


    commission_id=fields.Many2one('agent_commission')
    customer = fields.Many2one('res.partner', string='Customer', required=1)
    booking_info_id = fields.Many2one('tour_booking_information',string="Booking Information ID", )
    commission = fields.Integer(string="Commission")
    cost = fields.Integer(string="Cost")