# -*- coding: utf-8 -*-
{
    'name': "Open Academy",

    'summary': """Course Management""",

    'description': """
        Open Academy allow you to manage your course, session, teacher and attendee 
    """,

    'author': "PoulSociety",
    'website': "http://www.poulsociety.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Academy',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/course.xml',
        'views/session.xml',
        'views/partner.xml',
        'report/session.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}