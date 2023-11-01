from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ComapanyRecord(models.Model):
    _name = "company.company"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Company Records"

    # T00468 added field
    name = fields.Char(string="Company Name", required=True)
    image = fields.Image()
    address = fields.Text(string="Company Address", required=True)
    website = fields.Char()
    linkedin = fields.Char()
    job_position = fields.Text()
    job_description = fields.Text()
    contact = fields.Char()
    application_deadline = fields.Date()
    company_profile = fields.Text()
    student_ids = fields.Many2many(
        comodel_name="student.record",
        relation="",
        column1="",
        column2="",
    )
    package_offer = fields.Char(help="Annual Package Offer")
    campus_driven_date = fields.Date()

    @api.constrains("contact")
    def _check_mobile_no(self):
        """function to check mobile no is valid or not, otherwise show error #T00468"""
        if self.contact and len(self.contact.replace(" ", "")) != 10:
            raise ValidationError(_("Invalid Contact Number"))
