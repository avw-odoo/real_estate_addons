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
        return http.request.render('real_estate_property_website.listing', {
            'root': '/real-estate',
            'properties': http.request.env['real_estate.property'].search([]),
        })

    @http.route('/real-estate/properties/<model("real_estate.property"):obj>', auth='public', website=True)
    def object(self, obj, **kw):
        """ Route to display the details of a specific property. """
        return http.request.render('real_estate_property_website.property', {
            'property': obj
        })