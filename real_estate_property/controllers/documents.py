# -*- coding: utf-8 -*-
# Copyright (C) 2023 Alain van de Werve (avw82@icloud.com)

import logging

from odoo import http
from odoo.addons.documents.controllers.documents import ShareRoute
from odoo.http import request

class PropertyShareRoute(ShareRoute):

    def _create_uploaded_documents(self, files, share, folder, documents_values=None):
        documents_values = documents_values or {}
        property = folder._get_property_id()
        if property:
            documents_values.update({
                'res_model': 'real_estate.property',
                'res_id': property.id,
            })
        return super()._create_uploaded_documents(files, share, folder, documents_values)

    @http.route()
    def upload_document(self, folder_id, ufile, tag_ids, **kwargs):
        if not kwargs.get('res_model') and not kwargs.get('res_id'):
            current_folder = request.env['documents.folder'].browse(int(folder_id))
            property = current_folder._get_property_id()
            if property:
                kwargs.update({
                    'res_model': 'real_estate.property',
                    'res_id': property.id,
                })
        return super().upload_document(folder_id, ufile, tag_ids, **kwargs)
