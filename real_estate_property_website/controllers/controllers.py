#-*- coding: utf-8 -*-
import base64
import io

from odoo import http
from odoo.http import request

class RealEstateProperty(http.Controller):

    @http.route('/real-estate/', auth='public', website=True)
    def index(self, **kw):
        """Homepage route for the real estate website."""
        return "Website for Real Estate Property"

    @http.route('/real-estate/properties', auth='public', website=True)
    def list(self, **kw):
        """Route to list all real estate properties with their main image."""
        Property = request.env['real_estate.property']
        properties = Property.search([])
        properties_with_images = [(prop, self._get_main_image_for_property(prop)) for prop in properties]

        return request.render('real_estate_property_website.property_website_kanban_template', {
            'root': '/real-estate',
            'properties_with_images': properties_with_images,
        })

    @http.route('/real-estate/properties/<model("real_estate.property"):obj>', auth='public', website=True)
    def object(self, obj, **kw):
        """Route to display a single real estate property with its main and thumbnail images."""
        main_image, thumbnails = self._get_images_for_property(obj)
        if not main_image:
            # Redirect to a custom error page if the main image is not found.
            return request.render('real_estate_property_website.error_template', {
                'error_message': 'Main image for the property is not available.'
            })

        return request.render('real_estate_property_website.property_website_detail_template', {
            'property': obj,
            'main_image': main_image,
            'thumbnails': thumbnails,
        })

    def _get_images_for_property(self, property):
        """Fetches the main and thumbnail images for a property based on the defined tags."""
        Document = request.env['documents.document']
        top_photo_tag_id = self._get_tag_id('real_estate_property.documents_realestate_types_top_photo')
        photo_tag_id = self._get_tag_id('real_estate_property.documents_realestate_types_photo')
        distribution_website_tag_id = self._get_tag_id('real_estate_property.documents_realestate_distribution_website')

        if not all([top_photo_tag_id, photo_tag_id, distribution_website_tag_id]):
            # Log an error and return no images if any required tag is missing.
            self._log_missing_tags_error()
            return None, None

        main_image = Document.search([
            ('property_id', '=', property.id),
            ('tag_ids', '=', top_photo_tag_id),
            #('tag_ids', '=', distribution_website_tag_id) # we want simpler logic about the illustration
        ], limit=1)

        thumbnails = Document.search([
            ('property_id', '=', property.id),
            ('tag_ids', '=', photo_tag_id),
            ('tag_ids', '=', distribution_website_tag_id),
            ('id', 'not in', main_image.ids)
        ], limit=4) if main_image else None

        return main_image, thumbnails

    def _get_main_image_for_property(self, property):
        """Retrieves the main image for a property to be displayed in the list view."""
        main_image, _ = self._get_images_for_property(property)
        return main_image[0] if main_image else None

    def _get_tag_id(self, xml_id):
        """Safely fetches the ID of a tag, returning None if not found."""
        return request.env.ref(xml_id, raise_if_not_found=False).id

    def _log_missing_tags_error(self):
        """Logs an error message when required document tags are missing."""
        request.env['ir.logging'].create({
            'name': 'Real Estate Controller',
            'type': 'server',
            'level': 'ERROR',
            'dbname': request.env.cr.dbname,
            'message': 'One or more required document tags are missing.',
        })