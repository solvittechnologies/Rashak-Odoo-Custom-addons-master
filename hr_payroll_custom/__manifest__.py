# -*- coding:utf-8 -*-

{
    'name': 'HR PAYROLL CUSTOM',
    'version': '16.0',
    'author': 'Yves NGAH',
    'license': 'LGPL-3',
    'depends': [
        'hr',
        'hr_contract',
    ],
    'data': [
        
        'views/hr_payroll_views.xml',
        'views/hr_payroll_actions.xml',
        'views/hr_payroll_menu.xml',
        'views/hr_employee_view_custom.xml',
        

    ],
    'application': True,
}


#'security/hr_payroll_security.xml',
#        'security/ir.model.access.csv',