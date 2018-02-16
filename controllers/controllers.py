# -*- coding: utf-8 -*-
from odoo import http

class Openacademy(http.Controller):
    @http.route('/openacademy/', auth='public', website = True)
    def index(self, **kw):
        Teachers = http.request.env['openacademy.teachers']
        return http.request.render('openacademy.index', {
            'teachers': Teachers.search([])
        })

