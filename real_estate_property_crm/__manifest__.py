# -*- coding: utf-8 -*-
# Copyright (C) 2023 Alain van de Werve (avw82@icloud.com)


{
    'name': 'CRM for Real Estate Property',
    'version': '0.1',
    'category': 'Sales/Real Estate',
    'sequence': 25,
    'license': 'LGPL-3',
    'author': 'Alain van de Werve',
    'email': 'avw82@icloud.com',
    'summary': 'Enhance real estate management via CRM integration.',
    'website': 'https://www.odoo.com/app/',
    'depends': [
        'crm',
        'real_estate_property',
        ],
     'data': [
         'views/crm_lead_view.xml',
         'views/real_estate_property_views.xml',
     ],
    'installable': True,
}
