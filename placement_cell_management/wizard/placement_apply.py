from odoo import fields, models


class CompanyApplyWizard(models.TransientModel):
    _name = "company.apply.wizard"
    _description = "Company Apply Wizard"

    name = fields.Char(string="Student Name ")
    enrollment_no = fields.Char(string="Enrollment No.")

    def add_library(self):
        pass
