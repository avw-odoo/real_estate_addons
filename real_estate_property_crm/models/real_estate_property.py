# -*- coding: utf-8 -*-
# Copyright (C) 2023 Alain van de Werve (avw82@icloud.com)


from odoo import models, fields, api


class RealEstateProperty(models.Model):
    _inherit = 'real_estate.property'

    #Inverse One2many field for crm.lead
    crm_lead_ids = fields.One2many('crm.lead','property_id',string='Related Leads')
    crm_lead_count2 = fields.Integer(string="Leads Count 2",compute="_compute_crm_lead_count")

    def action_view_related_leads(self):
        """Create an action to view CRM leads related to the property.
        This method is typically used to trigger an action from a button click in a form view.

        Returns:
            dict: Action dictionary to open the CRM lead list view.
        """
        self.ensure_one() # Ensures that the method is called on a single record
        return {
            'type': 'ir.actions.act_window',
            'name': 'Related Leads',
            'res_model': 'crm.lead',
            'view_mode': 'tree,form,kanban',
            #'domain': [('real_estate_property_id', '=', self.id)],
            'context': {
                'default_property_id': self.id, # Set the default property for new leads
                'search_default_property_id': self.id}, # Filter to show only leads related to this property
        }


    @api.depends('crm_lead_ids')
    def _compute_crm_lead_count(self):
        """Compute the number of CRM leads related to this property.
        The result is stored in the `crm_lead_count2` field.

        """
        for record in self:
            # Counting the number of related CRM leads
            record.crm_lead_count2 = len(record.crm_lead_ids)
    