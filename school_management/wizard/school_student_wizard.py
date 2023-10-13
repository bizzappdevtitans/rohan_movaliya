# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class SchoolStudentWizard(models.TransientModel):
    _name = "school.student.wizard"
    _description = "School Student wizard"

    @api.model
    def default_get(self, field):
        """Set default value in wizards form view #T00356"""
        value = super(SchoolStudentWizard, self).default_get(field)
        active_id = self._context.get("active_id")
        record = self.env["school.student"].browse(active_id)
        value["name"] = record.name
        value["enrollment_no"] = record.enrollment_no
        return value

    # T00356 added fields
    name = fields.Char(string="Student Name ", readonly=True)
    enrollment_no = fields.Char(string="Enrollment No.", readonly=True)
    pass_active = fields.Boolean(string="Pass Activated")

    def add_library(self):
        """function to add student name into library section #T00356"""
        active_id = self._context.get("active_id")
        record = self.env["school.library"].browse(active_id)
        record.create(
            {
                "student_name": self.name,
                "enrollment_no": self.enrollment_no,
                "is_active": self.pass_active,
            }
        )

    def update_data(self):
        """function to update student library pass status #T00356"""
        record = self.env["school.library"].search(
            [("enrollment_no", "=", self.enrollment_no)]
        )
        record.write({"is_active": self.pass_active})
