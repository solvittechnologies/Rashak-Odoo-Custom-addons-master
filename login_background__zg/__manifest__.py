# -*- coding: utf-8 -*-
{
    'name': "Login Background Image",

    'summary': """
        Background Image For Odoo Login Page""",

    'description': """
        Set Login background Image
    """,

    'author': "Zero Gravity",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','web','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'login_background__zg/static/src/css/**/*',
        ]
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images': [
        'static/description/banner.png',
        'static/description/theme_screenshot.png'
    ],
}
