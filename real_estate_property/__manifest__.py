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
        'calendar',
        'contacts',
        'documents',
        ],
    'data': [
        'security/ir.model.access.csv',
        'data/templates.xml',
        'views/real_estate_property_views.xml',
        'views/res_config_settings_view.xml',
        'views/documents_document_views.xml',
        'data/categories.xml',
        'data/tags.xml',
        'data/stages.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'post_init_hook': '_generate_templates',
    'assets': {
        'web.assets_backend': [
            'real_estate_property/static/src/**/*',
        ],
    'installable': True,
    'application': True,
}}
