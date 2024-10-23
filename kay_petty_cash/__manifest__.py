# -*- coding: utf-8 -*-

{
    'name': 'Fastra Petty Cash',
    'version': '16.0.1.0.0',
    'summary': 'Fastra Petty Cash',
    'depends':  ['base', 'account','analytic'],
    'data': [
        'security/ir.model.access.csv',

        'views/kay_petty_cash.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
