# -*- coding: utf-8 -*-
################################################################################
#
#    Kolpolok Ltd. (https://www.kolpolok.com)
#    Author: Kaushik Ahmed Apu, Aqil Mahmud, Zarin Tasnim (<https://www.kolpolok.com>)
#
################################################################################
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import datetime


class PropertyRental(models.Model):
    """A class for the model property rental to represent
    the rental order of a property"""
    _name = 'property.rental'
    _description = 'Property Rent'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference', readonly=True,
                       required=True, copy=False, default='New',
                       help='The reference code/sequence of the property rental')
    property_id = fields.Many2one(
        'property.property', string='Property',
        required=True,
        help='The property to be rented',
        domain="[('state','=','available'),('sale_rent','=','for_tenancy')]")
    owner_id = fields.Many2one('res.partner', string='Land Lord',
                               related='property_id.landlord_id', store=True,
                               help='The owner / land lord of the property')
    rent_price = fields.Monetary(string='Rent Price',
                                 related='property_id.rent_month',
                                 help='The rental price per month of the property')
    maintenance_cost = fields.Monetary(string='Maintenance Cost', default=0.0,
                                       help='One-time maintenance cost included in the first bill')
    insurance_cost = fields.Monetary(string='Insurance Cost', default=0.0,
                                     help='One-time insurance cost included in the first bill')
    total_monthly_cost = fields.Monetary(string='Total Monthly Cost',
                                         compute='_compute_total_monthly_cost',
                                         store=True,
                                         help='Total monthly cost (rent only for subsequent months)')
    renter_id = fields.Many2one('res.partner', string='Renter', required=True,
                                help='The customer who is renting the property')
    state = fields.Selection(
        [('draft', 'Draft'), ('in_contract', 'In Contract'),
         ('expired', 'Expired'), ('cancel', 'Cancelled')],
        required=True, default='draft', string='Status', tracking=True,
        help="* The 'Draft' status is used when the rental is in draft.\n"
             "* The 'In Contract' status is used when the property is rented "
             "and is in contract\n"
             "* The 'Expired' status is used when the property rented "
             "contract has expired.\n"
             "* The 'Cancelled' status is used when the property rental "
             "is cancelled.\n")
    start_date = fields.Date(string='Start Date', required=True,
                             help='The starting date of the rent')
    end_date = fields.Date(string='End Date', required=True,
                           help='The ending date of the rent')
    invoice_count = fields.Integer(string='Invoice Count',
                                   compute='_compute_invoice_count',
                                   help='The invoices related to this rental')
    rental_bills_ids = fields.One2many('rental.bill', 'rental_id', string='Rental Bills')
    invoice_date = fields.Date(string='Last Invoice Date',
                               help='The latest invoiced date')
    next_invoice = fields.Date(string='Next Invoice',
                               compute='_compute_next_invoice',
                               help='The next invoicing date')
    company_id = fields.Many2one('res.company',
                                 string="Property Management Company",
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  related='company_id.currency_id')

    @api.model
    def create(self, vals):
        """Setting the sequence when record is created"""
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('property.rent') or 'New'
        res = super(PropertyRental, self).create(vals)
        return res

    @api.depends('rent_price', 'maintenance_cost', 'insurance_cost')
    def _compute_total_monthly_cost(self):
        """Compute the total monthly cost (rent only for subsequent months)"""
        for record in self:
            record.total_monthly_cost = record.rent_price

    def _compute_invoice_count(self):
        """Calculates the invoice count for the property"""
        for record in self:
            record.invoice_count = self.env['account.move'].search_count(
                [('property_rental_id', '=', record.id)])

    def _compute_next_invoice(self):
        """Computes the next invoice date"""
        for record in self:
            if record.invoice_date and fields.Date.today() < record.end_date:
                record.next_invoice = fields.Date.add(record.invoice_date, months=1)
            else:
                record.next_invoice = False

    def action_cancel(self):
        """Changes the record stage to cancel"""
        self.property_id.state = 'available'
        self.state = 'cancel'
        # Cancel related bills
        self.rental_bills_ids.filtered(lambda b: b.status != 'paid').write({'status': 'cancelled'})

    def action_create_contract(self):
        """Creates the initial invoice with all costs and generates monthly rent bills"""
        if self.renter_id.blacklisted:
            raise ValidationError(_('The Customer %r is Blacklisted.', self.renter_id.name))

        # Create the first invoice with rent, maintenance, and insurance
        self._create_first_invoice()
        self.invoice_date = self.start_date

        # Generate subsequent rent-only bills
        self._generate_monthly_rent_bills()

        self.property_id.state = 'rented'
        self.state = 'in_contract'

    def _create_first_invoice(self):
        """Creates the first invoice including rent, maintenance, and insurance"""
        invoice_lines = [
            fields.Command.create({
                'name': f"{self.property_id.name} - Monthly Rent",
                'price_unit': self.rent_price,
                'currency_id': self.env.user.company_id.currency_id.id,
            })
        ]
        bill_lines = [
            {'name': f"{self.property_id.name} - Monthly Rent", 'amount': self.rent_price, 'bill_date': self.start_date}
        ]
        if self.maintenance_cost > 0:
            invoice_lines.append(fields.Command.create({
                'name': f"{self.property_id.name} - Maintenance",
                'price_unit': self.maintenance_cost,
                'currency_id': self.env.user.company_id.currency_id.id,
            }))
            bill_lines.append({'name': f"{self.property_id.name} - Maintenance", 'amount': self.maintenance_cost,
                               'bill_date': self.start_date})
        if self.insurance_cost > 0:
            invoice_lines.append(fields.Command.create({
                'name': f"{self.property_id.name} - Insurance",
                'price_unit': self.insurance_cost,
                'currency_id': self.env.user.company_id.currency_id.id,
            }))
            bill_lines.append({'name': f"{self.property_id.name} - Insurance", 'amount': self.insurance_cost,
                               'bill_date': self.start_date})

        # Create the invoice
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'property_rental_id': self.id,
            'invoice_line_ids': invoice_lines,
            'invoice_date': self.start_date,
            'partner_id': self.renter_id.id,
        })

        # Sync with rental_bills_ids
        for line in bill_lines:
            self.env['rental.bill'].create({
                'rental_id': self.id,
                'name': line['name'],
                'amount': line['amount'],
                'bill_date': line['bill_date'],
                'bill_no': invoice.id,
                'status': 'invoiced',
            })

    def _generate_monthly_rent_bills(self):
        """Generates rent-only invoices for each month between start_date and end_date"""
        start = fields.Date.from_string(self.start_date)
        end = fields.Date.from_string(self.end_date)
        current_date = start + relativedelta(months=1)  # Start from the next month

        while current_date <= end:
            # Create the invoice
            invoice = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'property_rental_id': self.id,
                'invoice_line_ids': [fields.Command.create({
                    'name': f"{self.property_id.name} - Monthly Rent",
                    'price_unit': self.rent_price,
                    'currency_id': self.env.user.company_id.currency_id.id,
                })],
                'invoice_date': current_date,
                'partner_id': self.renter_id.id,
            })

            # Sync with rental_bills_ids
            self.env['rental.bill'].create({
                'rental_id': self.id,
                'name': f"{self.property_id.name} - Monthly Rent",
                'amount': self.rent_price,
                'bill_date': current_date,
                'bill_no': invoice.id,
                'status': 'invoiced',
            })

            current_date += relativedelta(months=1)

    def action_view_invoice(self):
        """Views all related invoices in tree view"""
        return {
            'name': _('Invoices'),
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'domain': [('property_rental_id', '=', self.id), ('move_type', '=', 'out_invoice')]
        }

    @api.model
    def action_check_rental(self):
        """Scheduled action to check for expired contracts"""
        records = self.env['property.rental'].search([('state', '=', 'in_contract')])
        for rec in records:
            if fields.Date.today() > rec.end_date:
                rec.state = 'expired'