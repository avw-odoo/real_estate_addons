# -*- coding: utf-8 -*-
# Copyright (C) 2023 Alain van de Werve (avw82@icloud.com)


{
    'name': 'Website for Real Estate Property',
    'version': '0.1',
    'category': 'Sales/Real Estate',
    'sequence': 25,
    'license': 'LGPL-3',
    'author': 'Alain van de Werve',
    'email': 'avw82@icloud.com',
    'summary': 'publish properties on your Website',
    'website': 'https://www.odoo.com/app/',
    'depends': [
        'website',
        'real_estate_property',
        ],
    'data': [
        'views/templates.xml',
        'views/real_estate_property_website_menu.xml',
    ],
    'installable': True,
}
