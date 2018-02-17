from odoo import models, fields, api


class Teachers(models.Model):

    """ Storing Teachers in Odoo Database """

    _name = 'openacademy.teachers'

    name = fields.Char()

    biography = fields.Html()