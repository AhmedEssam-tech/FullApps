from odoo import models, fields, api


class TourManagement(models.Model):
    _name = 'tour.management'
    _description = 'Tour Management'

    # Fields
    tour_consultant = fields.Many2one('res.partner', string='Tour Consultant')
    service = fields.Selection(
        [('cab', 'Cab'), ('bus', 'Bus'), ('flight', 'Flight')],
        string='Service',
        required=True
    )
    invoice_number = fields.Many2one('account.move',string='Invoice Number',domain=[('move_type', '=', 'out_invoice')])
    entrance_fee_given = fields.Float(string='Entrance Fee Given')
    entrance_fee_used = fields.Float(string='Entrance Fee Used')
    entrance_fee_to_return = fields.Float(
        string='Entrance Fee to be Returned',
        compute='_compute_entrance_fee_to_return',
        store=True
    )
    guide = fields.Many2one('res.partner', string='Guide')
    driver = fields.Many2one('res.partner', string='Driver')
    invoice_amount = fields.Float(string='Invoice Amount')
    extra_paid = fields.Float(string='Extra Paid')
    balance_amount = fields.Float(string='Balance Amount')
    transfer_tour_payment = fields.Float(string='Transfer Tour Payment')

    @api.depends('entrance_fee_given', 'entrance_fee_used')
    def _compute_entrance_fee_to_return(self):
        for record in self:
            record.entrance_fee_to_return = record.entrance_fee_given - record.entrance_fee_used
