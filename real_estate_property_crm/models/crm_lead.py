# -*- coding: utf-8 -*-
# Copyright (C) 2023 Alain van de Werve (avw82@icloud.com)

from odoo.tools import Markup
from odoo import api, models, fields, _


class CrmLead(models.Model):
    _inherit = 'crm.lead'


    # Define a Many2one relationship field to the real estate property
    property_id = fields.Many2one('real_estate.property', string='Interested in Property')

    def write(self, vals):
        # Perform the standard write operation and store the result
        res = super(CrmLead, self).write(vals)

        # Check if the 'real_estate_property_id' field is being updated
        if 'property_id' in vals:
            # Get the new property record
            new_property = self.env['real_estate.property'].browse(vals['property_id'])
            # If there is a new property, create a message to post in the chatter
            if new_property:
                message = _("Interested in property: ") + new_property._get_html_link()
                # Post the constructed message to the chatter
                self.message_post(body=message)

        # Return the result of the write operation
        return res