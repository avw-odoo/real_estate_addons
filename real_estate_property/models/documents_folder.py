# -*- coding: utf-8 -*-
# Copyright (C) 2023 Alain van de Werve (avw82@icloud.com)

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression



class DocumentFolder(models.Model):
    _inherit = 'documents.folder'

    def default_get(self, fields):
        res = super().default_get(fields)
        if self.env.context.get('documents_property') and not res.get('parent_folder_id'):
            res['parent_folder_id'] = self.env.ref('real_estate_property.documents_realestate_folder').id
        return res

    property_id = fields.Many2one('real_estate.property')


    @api.model
    def create(self, vals):
        # If a parent folder is defined, check whether it is linked to a property
        parent_folder_id = vals.get('parent_folder_id')
        if parent_folder_id:
            parent_folder = self.env['documents.folder'].browse(parent_folder_id)
            
            if parent_folder.property_id:
                # Assign the same property
                vals['property_id'] = parent_folder.property_id.id

        return super(DocumentFolder, self).create(vals)


    @api.ondelete(at_uninstall=False)
    def unlink_except_property_folder(self):
        property_folder = self.env.ref('real_estate_property.documents_realestate_folder')
        if property_folder in self:
            raise UserError(_('The "%s" workspace is required by the Real Estate Property application and cannot be deleted.', property_folder.name))
    

    def _get_property_id(self):
        if self.property_id:
            return self.property_id
        return self.env['real_estate.property']



class DocumentsTag(models.Model):
    _inherit = 'documents.tag'

    def unlink(self):
        protected_tags_ids = [
            self.env.ref('real_estate_property.documents_realestate_distribution_internal').id,
            self.env.ref('real_estate_property.documents_realestate_distribution_owner').id,
            self.env.ref('real_estate_property.documents_realestate_distribution_website').id,
            self.env.ref('real_estate_property.documents_realestate_distribution_notary').id,
            self.env.ref('real_estate_property.documents_realestate_types_photo').id,
        ]
        for record in self:
            if record.id in protected_tags_ids:
                raise UserError(
                    "This tag cannot be deleted because it is essential for folder sharing "
                    "and website integration. Deleting it could cause errors in the system."
                )
        return super(DocumentsTag, self).unlink()