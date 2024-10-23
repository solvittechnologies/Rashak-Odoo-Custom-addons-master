# -*- coding: utf-8 -*-
{
    'name': "Human Resource",

    'summary': """Consolidate HR menus into a single HR module.""",

    'category': 'Human Resource',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'hr_payroll', 'hr_expense', 'hr_attendance', 'hr_appraisal', 'hr_recruitment',
                'hr_holidays', 'web_notify', 'hr_work_entry_contract_enterprise'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/mail_template.xml',
        'hr_menus.xml',
        'employee_inherit_view.xml',
        'hr_expense_inherit_view.xml',
        'hr_payroll_inherit_view.xml'

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
