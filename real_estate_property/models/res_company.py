# -*- coding: utf-8 -*-
# Copyright (C) 2023 Alain van de Werve (avw82@icloud.com)


from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = "res.company"


    urban_planning_template = fields.Html(string='Urban planning template')