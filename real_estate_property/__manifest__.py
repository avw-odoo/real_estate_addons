# -*- coding: utf-8 -*-
# Copyright (C) 2023 Alain van de Werve (avw82@icloud.com)


{
    'name': 'Real Estate Property',
    'version': '0.1',
    'category': 'Sales/Real Estate',
    'license': 'LGPL-3',
    'author': 'Alain van de Werve',
    'email': 'avw82@icloud.com',
    'sequence': 25,
    'summary': 'Manage & publish properties on your Website & Real Estate Markets.',
    'website': 'https://www.odoo.com/app/',
    'depends': [
        'base_setup',
        'mail',
        'documents',
        'calendar',
        'contacts',
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/real_estate_property_views.xml',
        'views/res_config_settings_view.xml',
        'views/documents_document_views.xml',
        'data/categories.xml',
        'data/tags.xml',
        'data/stages.xml',
        'data/documents_folder_data.xml',
        'data/documents_facet_data.xml',
        'data/documents_tag_data.xml',
    ],
    'demo': [
        'demo/demo.xml',
        'demo/documents_demo.xml',
    ],
    'post_init_hook': '_assign_property_folder',
    'assets': {
        'web.assets_backend': [
            'real_estate_property/static/src/**/*',
        ],
    'installable': True,
    'application': True,
    
}}
