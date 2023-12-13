# -*- coding: utf-8 -*-
# Copyright (C) 2023 Alain van de Werve (avw82@icloud.com)

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression


class DocumentFolder(models.Model):
    _inherit = 'documents.folder'

    def default_get(self, fields):
        res = super().default_get(fields)
        if self.env.context.get('documents_project') and not res.get('parent_folder_id'):
            res['parent_folder_id'] = self.env.ref('real_estate_property.documents_realestate_folder').id
        return res

    property_ids = fields.One2many('real_estate.property', 'documents_folder_id')

    @api.ondelete(at_uninstall=False)
    def unlink_except_project_folder(self):
        property_folder = self.env.ref('real_estate_property.documents_realestate_folder')
        if property_folder in self:
            raise UserError(_('The "%s" workspace is required by the Real Estate Property application and cannot be deleted.', property_folder.name))
        