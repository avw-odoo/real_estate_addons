#-*- coding: utf-8 -*-
import base64
import io

from odoo import http
from odoo.http import request, Response

class RealEstateProperty(http.Controller):
    @http.route('/real-estate/', auth='public', website=True)
    def index(self, **kw):
        """ Route for the homepage of the real estate website. """
        return "Website for Real Estate Property"

    @http.route('/real-estate/properties', auth='public', website=True)
    def list(self, **kw):
        """ Route to list all real estate properties. """
        return http.request.render('real_estate_property_website.property_website_kanban_template', {
            'root': '/real-estate',
            'properties': http.request.env['real_estate.property'].search([]),
        })

    # @http.route('/real-estate/properties/<model("real_estate.property"):obj>', auth='public', website=True)
    # def object(self, obj, **kw):
    #     """ Route to display the details of a specific property. """
    #     return http.request.render('real_estate_property_website.property_website_detail_template', {
    #         'property': obj
    #     })
    
    @http.route('/real-estate/properties/<model("real_estate.property"):obj>', auth='public', website=True)
    def object(self, obj, **kw):
        Document = request.env['documents.document']
        photo_tag_id = request.env.ref('real_estate_property.documents_realestate_types_photo').id

        # Récupère tous les documents avec le tag photo pour la propriété donnée
        documents = Document.search([
            ('property_id', '=', obj.id),
            ('tag_ids', 'in', photo_tag_id)
        ], limit=5)

        # Sépare l'image principale et les vignettes
        main_image = documents[:1]
        thumbnails = documents[1:5] if len(documents) > 1 else Document

        return request.render('real_estate_property_website.property_website_detail_template', {
            'property': obj,
            'main_image': main_image,
            'thumbnails': thumbnails,
        })