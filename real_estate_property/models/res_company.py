# -*- coding: utf-8 -*-
# Copyright (C) 2023 Alain van de Werve (avw82@icloud.com)


from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = "res.company"


    urban_planning_template = fields.Html(string='Urban planning template')
    
    
    @api.model
    def _get_default_urban_planning_template(self):
        """Retrieve the default urban planning template rendered as HTML.
        This method uses the QWeb rendering engine to generate the template.

        Returns:
            str: The rendered HTML template for urban planning.
        """
        # Render the 'urban_template' QWeb template from 'real_estate_property' module
        return self.env['ir.qweb']._render('real_estate_property.urban_template')
        

    @api.model_create_multi
    def create(self, vals_list):
        """Override the create method to set the default urban planning template.
        This method is called when new records are created.

        Args:
            vals_list (list): List of dictionaries containing the data for new records.

        Returns:
            recordset: The newly created record(s).
        """
        # Create the new record(s) using the standard logic
        res = super().create(vals_list)

        # Update the newly created record(s) with the default urban planning template
        res.sudo().write({
            'urban_planning_template': self._get_default_urban_planning_template(),
        })
        return res    