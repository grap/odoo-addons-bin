# -*- coding: utf-8 -*-
{
    'name': 'Shop Opening Times',
    'version': '0.2',
    'category': 'Sales',
    'description': """
Provide opening times for shops
===============================

Functionnalities :
------------------
    * Add the possibility to provide opening times for shop per week ;
    * Opening times has begin date and optional end date to manage changes in opening times ;
    * Opening times provides a computed total hours field ;

Technical informations :
------------------------
    * Use ISO 8601 encoding weeks (http://en.wikipedia.org/wiki/ISO_8601) : The week begins by Monday (1) and ends by Sunday (7) ; 

Contacts :
----------
    * Sylvain LE GAL (https://twitter.com/legalsylvain); 
    * <informatique@grap.coop> for any help or question about this module.
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        ],
    'init_xml': [],
    'update_xml': [
        'security/ir_model_access_data.yml',
        'security/ir_rule_data.yml',
        'view/shop_opening_time_view.xml',
        'view/shop_opening_time_action.xml', 
        'view/shop_opening_time_menu.xml', 
        ],
    'demo_xml': [
        'demo/shop_opening_time_demo.yml',
    ],
    'js': [],
    'css': [],
    'qweb': [],
    'images': [],
    'post_load': '',
    'application': True,
    'installable': True,
    'auto_install': False,
    'images': ['static/src/img/screenshots/1.png'],
}
