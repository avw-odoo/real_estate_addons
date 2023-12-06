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
            # Sets property_id only if the related model is 'real_estate.property'
            record.property_id = record.res_model == 'real_estate.property' and self.env['real_estate.property'].browse(record.res_id)
    


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