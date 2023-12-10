# -*- coding: utf-8 -*-
# Copyright (C) 2023 Alain van de Werve (avw82@icloud.com)


import datetime
from odoo import models, fields, api

class RealEstateProperty(models.Model):
    _name = 'real_estate.property'
    _description = 'Real Estate Property'
    _inherit = ['mail.activity.mixin', 'format.address.mixin', "mail.thread"]


    # Get the html template from the company settings as default value
    @api.model
    def _get_default_urban_planning(self):
        company = self.env.company

        return company.urban_planning_template
    
    # Get all the stages
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        
        return self.env['real_estate.stage'].search([])
    
    # Set the first stage as default
    @api.model
    def _get_default_stage_id(self):

        return self.env['real_estate.stage'].search([], limit=1)


    # =========================================================
    # TAB General information
    # =========================================================
    name = fields.Char("Property Name", required=True)
    property_image = fields.Image("Illustration", max_height=300)
    
    # Link with Documents app
    document_ids = fields.One2many('documents.document', 'property_id', string='Documents')
    document_count = fields.Integer(compute='_compute_document_count')

    # needed for the Kanban view
    stage_id = fields.Many2one('real_estate.stage', ondelete='restrict', default=_get_default_stage_id,
        group_expand='_read_group_stage_ids', tracking=True, copy=False)
    kanban_state = fields.Selection([
        ('normal', 'Grey'),
        ('done', 'Green'),
        ('blocked', 'Red')], string='Kanban State',
        copy=False, default='normal', required=True)
    legend_blocked = fields.Char(related='stage_id.legend_blocked', string='Kanban Blocked')
    legend_done = fields.Char(related='stage_id.legend_done', string='Kanban Valid')
    legend_normal = fields.Char(related='stage_id.legend_normal', string='Kanban Ongoing')
    
    # Address
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")

    # Owner
    partner_id = fields.Many2one('res.partner', string='Owner', tracking=True)
    owner_email = fields.Char(related='partner_id.email', string="Email", readonly=False, store=True, tracking=True)
    owner_mobile = fields.Char(related='partner_id.mobile', string="Mobile", readonly=False, store=True, tracking=True)

    # Representative & Notes
    user_id = fields.Many2one('res.users', string='Real Estate Agent', default=lambda self: self.env.user, tracking=True)
    description = fields.Html(string='Internal notes')
    
    # =========================================================
    # TAB Finance
    # =========================================================
    transaction_type = fields.Selection([
        ('1','Sell'),
        ('2','Rent'),
        ('3','Other'),
    ], string='Type of Transaction', default='1', help="The specific type of sale or rental.")

    availabilty = fields.Selection([
        ('1','Undefined'),
        ('2','Available as of'),
        ('3','Immediately'),
        ('4','After signing the deed'),
        ('5','To be defined'),
        ('6','At delivery'),
        ('7','Depending on the tenant'),
    ], string='Availability', default='1')
    available_from = fields.Date()

    company_id = fields.Many2one('res.company', string='Company', store=True, readonly=False, default=lambda self: self.env.company)
    company_currency_id = fields.Many2one(string='Company Currency', related='company_id.currency_id', readonly=True)
    price = fields.Monetary('Selling Price',currency_field='company_currency_id', tracking=True)
    make_offer = fields.Boolean('Offers starting at')
    expected_revenue = fields.Monetary('Expected Revenue', currency_field='company_currency_id', tracking=True)
    
    # =========================================================
    # TAB Main features
    # =========================================================
    type_id = fields.Many2one('real_estate.type', string='Type', help="The type of the property. Estate type should have matching estate subtype.")
    subtype_id = fields.Many2one('real_estate.subtype', string='Subtype', help="Subtype to specify the selected estatetype in detail.")
    construction_year = fields.Selection(selection='get_years_choices', string='Year of Construction')
    frontages_number = fields.Selection([
        ('not_specified', 'Not Specified'),
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
    ], default='not_specified', string='Number of Frontages')
    frontage_width = fields.Char('Frontage Width')
    building_footprint = fields.Char('Building Footprint', help="The area of a plot of land covered by a building, measured from its external walls.")
    livable_area = fields.Char('Livable Area', help="Space within a property suitable for regular living, including bedrooms, living rooms, and kitchens, but excluding areas like garages and unfinished basements.")
    floor_number = fields.Char('Number of Floors')
    building_condition = fields.Selection([
        ('1','Good'),
        ('2','As new'),
        ('3','To restore'),
        ('4','Just renovated'),
        ('5','To refurbish'),
        ('6','To renovate'),
        ('7','Not Specified'),
    ], string='Building Condition', default='7')
    
    # Land orientation
    rear_facade_orientation = fields.Selection([
        ('not_specified', 'Not Specified'),
        ('1','North'),
        ('2','South'),
        ('3','East'),
        ('4','West'),
        ('5','Northeast'),
        ('6','Northwest'),
        ('7','Southeast'),
        ('8','Southwest'),
    ], default='not_specified', string='Rear Facade Orientation')
    land_area = fields.Char('Land Area', help="the total surface area of a piece of land, measured in square meters (m²) or acres.")
    land_width = fields.Char('Land width', help="distance across a piece of land at its widest point.")

    # Garden features
    garden = fields.Selection([
        ('not_specified', 'Not Specified'),
        ('1','Yes'),
        ('2','No'),
    ], default='not_specified', string='Garden')
    garden_orientation = fields.Selection([
        ('not_specified', 'Not Specified'),
        ('1','North'),
        ('2','South'),
        ('3','East'),
        ('4','West'),
        ('5','Northeast'),
        ('6','Northwest'),
        ('7','Southeast'),
        ('8','Southwest'),
    ], default='not_specified', string='Garden Orientation')

    # Terrace features
    terrace = fields.Selection([
        ('not_specified', 'Not Specified'),
        ('1','Yes'),
        ('2','No'),
    ], default='not_specified', string='Terrace')
    terrace_area = fields.Char('Terrace Area')
    terrace_orientation = fields.Selection([
        ('not_specified', 'Not Specified'),
        ('1','North'),
        ('2','South'),
        ('3','East'),
        ('4','West'),
        ('5','Northeast'),
        ('6','Northwest'),
        ('7','Southeast'),
        ('8','Southwest'),
    ], default='not_specified', string='Terrace Orientation')

    # Rooms
    basement = fields.Selection([
        ('not_specified', 'Not Specified'),
        ('1','Yes'),
        ('2','No'),
    ], string='Cellar', default='not_specified')
    attic = fields.Selection([
        ('not_specified', 'Not Specified'),
        ('1','Yes'),
        ('2','No'),
    ], string='Attic', default='not_specified')
    attic_type = fields.Selection([
        ('not_specified', 'Not Specified'),
        ('1','Finished attic'),
        ('2','Unfinished attic'),
        ('3','Attic suitable for conversion'),
    ], string='Attic type', default='not_specified')
    bedroom = fields.Char(string="# Bedroom")
    bathroom = fields.Char(string="# Bathroom")
    office = fields.Char(string="# Office")
    professional_practice = fields.Selection([
        ('not_specified', 'Not Specified'),
        ('1','Yes'),
        ('2','No'),
    ], default='not_specified', string='Professional practice')
    toilet = fields.Char(string="# Toilet")
    garage = fields.Char(string="# Garage")
    carport = fields.Char(string="# Carport")
    indoor_parking = fields.Char(string="# Indoor parking")
    outdoor_parking = fields.Char(string="# Outdoor parking")

    # Extra information
    property_extra_ids = fields.Many2many('real_estate.extra.tag', string='Extra information')
    
    # =========================================================
    # TAB Urban planning
    # =========================================================
    urban_planning = fields.Html(string='Urban planning', default=_get_default_urban_planning)
    # Land registry
    cadastre_section = fields.Char("Cadastre section")
    cadastre_number = fields.Char("Cadastre number")

    # =========================================================
    # TAB Visits & Participants
    # =========================================================
    visits = fields.Html(string='Visits')
    participants = fields.Html(string='Participants')

    # =========================================================
    # TAB Composition & Materials
    # =========================================================
    composition_ids = fields.One2many('real_estate.room', 'property_id', string='Composition')
    
    
    # Method to get choices for years
    def get_years_choices(self):
        current_year = datetime.date.today().year
        return [(str(year), str(year)) for year in reversed(range(1900, current_year + 1))]
    
    @api.model
    def _get_default_urban_planning(self):
        """Retrieve the default urban planning template from the current company.
        This is used as a default value for new real estate properties.

        Returns:
            str: Urban planning template as a string (HTML or text).
        """
        company = self.env.company
        return company.urban_planning_template
    
    def action_view_documents(self):
        """Create an action to view related documents for the property.
        This is typically used in a button click in the form view.

        Returns:
            dict: Action dictionary to open the document list view.
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Documents 2',
            'res_model': 'documents.document',
            'view_mode': 'kanban,tree,form',
            'context': {
                'default_property_id': self.id,
                'search_default_property_id': self.id,
                'default_res_model': 'real_estate.property', 'default_res_id': self.id,}
        }

    def _compute_document_count(self):
        """Compute the number of documents related to this property.
        The result is stored in the `document_count` field.
        """
        Document = self.env['documents.document']
        for record in self:
            record.document_count = Document.search_count([('property_id', '=', record.id)])
    
    @api.model
    def write(self, vals):
        """Override the standard write method to reset the Kanban state when the stage changes.

        Args:
            vals (dict): Dictionary of values to write.

        Returns:
            bool: True if the write operation is successful.
        """
        if "stage_id" in vals and "kanban_state" not in vals:
            vals["kanban_state"] = "normal"
        return super(RealEstateProperty, self).write(vals)
    


class RealEstateType(models.Model):
    _name = 'real_estate.type'
    _description = 'Real Estate Type'

    name = fields.Char("Type", required=True, translate=True)



class RealEstateSubtype(models.Model):
    _name = 'real_estate.subtype'
    _description = 'Real Estate Subtype'

    name = fields.Char("Subtype", required=True, translate=True)
    type_id = fields.Many2one('real_estate.type', string='Type', required=True)



class RealEstateExtraTag(models.Model):
    _name = 'real_estate.extra.tag'
    _description = 'Real Estate Extra Information'

    name = fields.Char("Extra Information", required=True, translate=True)
    color = fields.Integer()



class RealEstatePropertyRoom(models.Model):
    _name = 'real_estate.room'
    _description = 'Real Estate Room'

    name = fields.Selection([
        ('not_specified', 'Not Specified'),
        ('entrance_hall', 'Entrance hall'),
        ('night_hall', 'Night hall'),
        ('living_room', 'Living room'),
        ('kitchen', 'Kitchen'),
        ('equipped_kitchen', 'Equipped kitchen'),
        ('semi_equipped_kitchen', 'Semi-equipped kitchen'),
        ('fully_equipped_kitchen', 'Fully equipped kitchen'),
        ('new_kitchen', 'New kitchen'),
        ('breakfast_nook', 'Breakfast nook'),
        ('dining_room', 'Dining room'),
        ('bedrooms', 'Bedrooms'),
        ('shower_room', 'Shower room'),
        ('bathrooms', 'Bathrooms'),
        ('toilets', 'Toilets'),
        ('playroom', 'Playroom'),
        ('office', 'Office'),
        ('laundry_room', 'Laundry room'),
        ('storage_room', 'Storage room'),
        ('garage', 'Garage'),
        ('parking', 'Parking'),
        ('terrace', 'Terrace'),
        ('garden', 'Garden'),
        ('cellar', 'Cellar'),
        ('pantry', 'Pantry'),
        ('storage_cellar', 'Storage cellar'),
        ('attic', 'Attic'),
        ('storage_attic', 'Storage attic'),
        ('commercial_space', 'Commercial space'),
        ('boiler', 'Boiler'),
        ('sauna', 'Sauna'),
        ('veranda', 'Veranda'),
        ('dressing', 'Dressing'),
        ('workshop', 'Workshop'),
        ('garden_chalet', 'Garden chalet'),
    ], string='Description', default='not_specified')
    floor_level = fields.Selection([
        ('cellars_3', 'Cellars -3'),
        ('cellars_2', 'Cellars -2'),
        ('cellars_1', 'Cellars -1'),
        ('outdoor_fittings', 'Outdoor fittings'),
        ('ground_floor', 'Ground floor'),
        ('garden_level', 'Garden level'),
        ('mezzanine_floor', 'Mezzanine floor'),
        ('attic', 'Attic'),
        ('first_floor', 'First floor'),
        ('mezzanine', 'Mezzanine'),
        ('second_floor', 'Second floor'),
        ('third_floor', 'Third floor'),
        ('fourth_floor', 'Fourth floor'),
    ], string='Floor Level', default='ground_floor', required=True)
    room_area = fields.Integer('Room Area')
    room_condition = fields.Selection([
        ('not_specified', 'Not Specified'),
        ('new', 'New'),
        ('perfect', 'Perfect'),
        ('good', 'Good'),
        ('moderate', 'Moderate'),
        ('to_refresh', 'To refresh'),
        ('to_restore', 'To restore'),
    ], string='Room Condition', default='not_specified')
    floor_type = fields.Selection([
        ('not_specified', 'Not Specified'),
        ('wooden_floor', 'Wooden floor'),
        ('tiles', 'Tiles'),
        ('carpet', 'Carpet'),
        ('lamination', 'Lamination'),
        ('cork', 'Cork'),
        ('floorboards', 'Floorboards'),
        ('linoleum', 'Linoleum'),
        ('pvc', 'PVC'),
        ('marble', 'Marble'),
        ('natural_stone', 'Natural stone'),
        ('industrial_tiles', 'Industrial tiles'),
        ('distribution_screed', 'Distribution screed'),
        ('screed', 'Screed'),
        ('polished_concrete', 'Polished concrete'),
        ('vinyl', 'Vinyl'),
        ('concrete', 'Concrete'),
        ('carpet_tiles', 'Carpet tiles'),
    ], string='Floor Type', default='not_specified')
    comment = fields.Text('Comment')
    property_id = fields.Many2one('real_estate.property', 'Property', required=True, ondelete='cascade')