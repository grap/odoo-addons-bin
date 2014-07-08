# -*- coding: utf-8 -*-

{
    'name': 'GRAP - migration update',
    'version': '0.1',
    'category': 'GRAP - Migration',
    'description': """
        Update the object of the framework.
        rules,
    """,
    'author': 'Sylvain LE GAL / Julien WESTE - Groupement Régional Alimentaire de Proximité (GRAP)',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'account',
        'stock',
        'account_fiscal_company',
        'point_of_sale',
        ],
    'init_xml': [
        ],
    'update_xml': [
        'ir_rule_data.xml',
        'stock_location_data.xml',
        'sale_shop_data.xml',
        'ir_property_data.xml',
        ],
    'demo_xml': [],
    'active': False,
    'installable': True,
    'application': True,
    'complexity': "easy",
}
