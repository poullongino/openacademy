# -*- coding: utf-8 -*-
from odoo import http

class Openacademy(http.Controller):
    @http.route('/openacademy/', auth='public', website = True)
    def index(self, **kw):
        Teachers = http.request.env['openacademy.teachers']
        return http.request.render('openacademy.index', {
            'teachers': Teachers.search([])
        })


    @http.route('/openacademy/<model("openacademy.teachers"):teacher>/', auth = 'public', website = True)
    def teacher(self, teacher):

        """ Returning Records when given their id """

        return http.request.render('openacademy.biography', {
            'person': teacher
        })

