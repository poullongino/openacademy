# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _

class Session(models.Model):
    _name = 'openacademy.session'

    name = fields.Char(required=True)
    start_date = fields.Date(default=lambda self : fields.Date.today())
    duration = fields.Float(digits=(6, 2), help="Duration in days", default=1)
    seats = fields.Integer(string = "Number of seats")
