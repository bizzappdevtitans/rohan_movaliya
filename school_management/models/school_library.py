from datetime import date

from odoo import fields, models


class SchoolLibrary(models.Model):
    _name = "school.library"
    _description = "Library of School"
    _rec_name = "enrollment_no"

    # T00356 added fields
    student_name = fields.Char()
    enrollment_no = fields.Char()
    is_active = fields.Boolean(string="Library Pass Activated")
    pass_active_date = fields.Date(default=date.today())

    def disable_library_pass(self):
        """mathod for automated action #T00432"""
        record = self.search([("is_active", "=", "True")])
        for check in record:
            if (date.today() - check.pass_active_date).days > 90:
                check.is_active = False
