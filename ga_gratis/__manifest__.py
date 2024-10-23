# -*- coding: utf-8 -*-
{
    "name": "Gratis",
    "summary": """Odoo without charges""",
    "description": """
        Odoo without charges
    """,
    "author": "My Company",
    "website": "http://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "hidden",
    "version": "1.0",
    # any module necessary for this one to work correctly
    "depends": ["base", "mail"],
    # always loaded
    "data": [
        # 'security/ir.model.access.csv',
        "data/views.xml",
        "data/templates.xml",
    ],
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
}
