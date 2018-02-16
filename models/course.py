# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Course(models.Model):
    _name = 'openacademy.course'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")
    level = fields.Selection([
        (1, 'Easy'),
        (2, 'Medium'),
        (3, 'Hard'),
    ], string = "Difficulty Level")
    session_count = fields.Integer("Session Count", compute = "_compute_session_count")
    
    @api.multi
    def copy(self, default = None):

        """ Copy Method which allow to duplicate the course Title """

        default = dict(default or {})

        copied_count =  self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))]
        )
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)
            
    
    @api.depends('session_ids')
    def _compute_session_count(self):

        """ COMPUTE THE TOTAL SESSIONS FOR A COURSE """
        for course in self:
            course.session_count = len(course.session_ids)


    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         'The title of the course should not be the description'),
        
        ('name_unique',
         'UNIQUE(name)',
         "The course title must be unique"),
    ]

