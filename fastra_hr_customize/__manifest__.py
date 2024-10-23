# -*- coding: utf-8 -*-

{
    'name': 'Fastra HR Customize',
    'version': '16.0.1.0.0',
    'summary': 'Fastra HR Customize',
    'depends': ['hr', 'hr_menus', 'account', 'stock'],
    'data': [
        'security/ir.model.access.csv',

        'data/payroll_sequence.xml',

        'views/hr_payslip_custom.xml',

        'wizards/payslip_line_print_wizard.xml',

        'reports/report.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
