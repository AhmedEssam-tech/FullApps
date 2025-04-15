
from odoo import models, fields


class JobCard(models.Model):
    _name = 'job.card'
    _description = 'Job Card'

    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    customer_email = fields.Char(related='customer_id.email', string='Customer Email', readonly=True)
    customer_phone = fields.Char(related='customer_id.phone', string='Customer Phone', readonly=True)
    assign_to = fields.Many2one('res.users', string='Assign To')
    jobcard_number = fields.Char(string='Jobcard Number', required=True, copy=False, readonly=True,
                                 default=lambda self: self.env['ir.sequence'].next_by_code('job.card'))
    jobcard_subject = fields.Char(string='Jobcard Subject')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    currency_id = fields.Many2one('res.currency', string='Currency')
    jobcard_status = fields.Selection(
        [('draft', 'Draft'), ('in_progress', 'In Progress'), ('done', 'Done')],
        string='Status',
        default='draft'
    )
    technician_name = fields.Char(string='Technician Name')
    technician_date = fields.Date(string='Technician Date')
    customer_representative_name = fields.Char(string='Customer Representative Name')
    customer_representative_date = fields.Date(string='Customer Representative Date')
