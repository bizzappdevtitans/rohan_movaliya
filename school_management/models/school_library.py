# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SchoolLibrary(models.Model):
    _name = "school.library"
    _description = "Library of School"
    _rec_name = "enrollment_no"

    # T00356 added fields
    student_name = fields.Char(string="Name")
    enrollment_no = fields.Char(string="Reference")
    is_active = fields.Boolean(string="Library Pass")
