# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    urban_planning_template = fields.Html(related='company_id.urban_planning_template', readonly=False)
    module_real_estate_property_crm = fields.Boolean(string='Add the crm power')
    module_real_estate_property_website = fields.Boolean(string='Add the website power')
