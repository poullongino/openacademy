# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import models, fields, api, exceptions, _


class Session(models.Model):

    """ Session Model """
    _name = 'openacademy.session'

    name = fields.Char(required = True)
    start_date = fields.Date(default = fields.Date.today)
    end_date = fields.Date(string = "End Date", store = True,
                           compute = "_get_end_date", inverse = '_set_end_date')
    duration = fields.Float(digits = (6, 2), help = "Duration in days", default = 1)
    seats = fields.Integer(string = "Number of seats")
    instructor_id = fields.Many2one('res.partner', string = "Instructor",
                                    domain=['|', ('instructor', '=', True),
                                            ('category_id.name', 'ilike', 'Teacher')])
    course_id = fields.Many2one('openacademy.course', ondelete = 'cascade', string = "Course", required = True)
    attendee_ids = fields.Many2many('res.partner', string = "Attendees")
    taken_seats = fields.Float(string = "Taken Seats", compute = "_taken_seats")
    active = fields.Boolean(default = True)
    color = fields.Integer()


    def _warning(self, title, message):

        """ Function to Display Warnings """

        return {'warning': {
            'title': title,
            'message': message,
        }}


    def _set_end_date(self):

        """
            Setting End Date
            Compute the difference between dates, but: Friday - Monday = 4 days,
            so add one day to get 5 days instead
        """

        for r in self:
            if not (r.start_date and r.end_date):
                continue

                start_date = fields.Datetime.from_string(r.start_date)
                end_date = fields.Datetime.from_string(r.end_date)
                r.duration = (end_date - start_date).days + 1


    @api.multi
    def copy(self, default=None):

        """ Copy Method which allow to duplicate The Session Title """

        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"Copy of {}%".format(self.name))]
        )
        if not copied_count:
            new_name = u"Copy of {}".format(self.name)
        else:
            new_name = u"Copy of {} ({})".format(self.name, copied_count)

        default['name'] = new_name
        return super(Session, self).copy(default)


    @api.depends("seats", "attendee_ids")
    def _taken_seats(self):

        """ Compute Taken Seats in Percentages """

        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats


    @api.depends('start_date', 'duration')
    def _get_end_date(self):

        """
            Compute End Date
            Add duration to start_date, but: Monday + 5 days = Saturday, so
            subtract one second to get on Friday instead
        """

        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue

                start = fields.Datetime.from_string(r.start_date)
                duration = timedelta(days = r.duration, seconds = -1)
                r.end_date = start + duration


    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):

        """ Explicit Onchange to Warn about Invalid Seats """

        if self.seats < 0:
            return self._warning("Incorrect 'seats' value",  "The number of available seats may not be negative")
        if self.seats < len(self.attendee_ids):
            return self._warning("Too many attendees", "Increase seats or remove excess attendees")


    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):

        """
           a constraint that checks that the instructor is not present in the attendees of his/her own session
        """

        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise exceptions.ValidationError("A session's instructor can't be an attendee")


    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "The session title must be unique"),
    ]