from odoo import api, fields, models



class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_sub_agent = fields.Boolean(string='Is a Sub Agent')
    is_agent = fields.Boolean(string='Is an Agent')
    is_guide = fields.Boolean(string='Is a Guide')
    is_driver = fields.Boolean(string='Is a Driver')
    is_tour_consultant = fields.Boolean(string='Is a Tour Consultant')
    is_other_contact = fields.Boolean(string='Other Contact')
    agent_code = fields.Char(string='GSTIN')

