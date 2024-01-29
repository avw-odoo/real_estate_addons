# -*- coding: utf-8 -*-
# Copyright (C) 2023 Alain van de Werve (avw82@icloud.com)


from odoo import models, fields, api
from odoo.addons.http_routing.models.ir_http import slug



class RealEstateProperty(models.Model):
    _name = 'real_estate.property'
    _inherit = [
        'real_estate.property',
        'website.published.mixin',
    ]

    is_published = fields.Boolean(tracking=True)


    def _compute_website_url(self):
        super(RealEstateProperty, self)._compute_website_url()
        for property in self:
            if property.id:  # avoid to perform a slug on a not yet saved record in case of an onchange.
                property.website_url = "/real-estate/properties/%s" % slug(property)
