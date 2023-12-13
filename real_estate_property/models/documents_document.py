# -*- coding: utf-8 -*-
# Copyright (C) 2023 Alain van de Werve (avw82@icloud.com)


from collections import OrderedDict
from odoo import _, models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.sql import SQL

class Document(models.Model):
    _inherit = 'documents.document'


    property_id = fields.Many2one('real_estate.property', compute='_compute_property_id', search='_search_property_id')


    @api.depends('res_id', 'res_model')
    def _compute_property_id(self):
        """Compute the `property_id` field based on the `res_id` and `res_model`.
        This method links a generic record to a specific real estate property record
        if `res_model` is 'real_estate.property'.

        """
        for record in self:
            record.property_id = record.res_model == 'real_estate.property' and self.env['real_estate.property'].browse(record.res_id)
    
    @api.model
    def search_panel_select_range(self, field_name, **kwargs):
        if field_name != 'folder_id' or not self._context.get('limit_folders_to_property'):
            return super().search_panel_select_range(field_name, **kwargs)

        res_model = self._context.get('active_model')
        if res_model != 'real_estate.property':
            return super().search_panel_select_range(field_name, **kwargs)

        res_id = self._context.get('active_id')
        fields = ['display_name', 'description', 'parent_folder_id', 'has_write_access']

        active_record = self.env[res_model].browse(res_id)
        if not active_record.exists():
            return super().search_panel_select_range(field_name, **kwargs)
        property = active_record if res_model == 'real_estate.property' else active_record.sudo().property_id

        document_read_group = self.env['documents.document']._read_group(kwargs.get('search_domain', []), [], ['folder_id:array_agg'])
        folder_ids = document_read_group[0][0]
        records = self.env['documents.folder'].with_context(hierarchical_naming=False).search_read([
            '|',
                ('id', 'child_of', property.documents_folder_id.id),
                ('id', 'in', folder_ids),
        ], fields)
        available_folder_ids = set(record['id'] for record in records)

        values_range = OrderedDict()
        for record in records:
            record_id = record['id']
            if record['parent_folder_id'] and record['parent_folder_id'][0] not in available_folder_ids:
                record['parent_folder_id'] = False
            value = record['parent_folder_id']
            record['parent_folder_id'] = value and value[0]
            values_range[record_id] = record

        return {
            'parent_field': 'parent_folder_id',
            'values': list(values_range.values()),
        }

    @api.model
    def _search_property_id(self, operator, value):
        """Custom search method for the `property_id` field.
        This method supports searching by boolean, integer, list, or string.

        Args:
            operator (str): The operator for the search (e.g., '=', '!=', 'ilike').
            value (bool|int|list|str): The value to search for.

        Returns:
            list: Domain criteria for the search operation.

        Raises:
            ValidationError: If the search operation is not valid.

        """

        # Boolean search, typically for existence checks
        if operator in ('=', '!=') and isinstance(value, bool):
            if not value:
                operator = operator == "=" and "!=" or "="
            return [
                ("res_model", operator, "real_estate.property"),
            ]
        
        # Search by record ID or list of IDs
        elif operator in ('=', '!=', "in", "not in") and (isinstance(value, int) or isinstance(value, list)):
            return [
                "&", ("res_model", "=", "real_estate.property"), ("res_id", operator, value),
            ]
        
         # Search by name or other string fields
        elif operator in ("ilike", "not ilike", "=", "!=") and isinstance(value, str):
            query_task = self.env["real_estate.property"]._search([(self.env["real_estate.property"]._rec_name, operator, value)])
            document_property_alias = query_task.make_alias('real_estate_property', 'document')
            query_task.add_join("JOIN", document_property_alias, 'documents_document', SQL(
                "%s = %s AND %s = %s",
                SQL.identifier('real_estate_property', 'id'),
                SQL.identifier(document_property_alias, 'res_id'),
                SQL.identifier(document_property_alias, 'res_model'),
                'real_estate.property',
            ))
            return [
                ("id", "inselect", query_task.select(f"{document_property_alias}.id")),
            ]
        
        # Raise an error for unsupported search types
        else:
            raise ValidationError(_("Invalid property search"))