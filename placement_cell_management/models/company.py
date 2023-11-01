from odoo import fields, models


class ComapanyRecord(models.Model):
    _name = "company.company"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Company Details"

    # T00468 added field
    name = fields.Char(string="Company Name", required=True)
    image = fields.Image()
    address = fields.Text(string="Company Address", required=True)
    website = fields.Char()
    linkedin = fields.Char()
    job_position = fields.Text()
    job_description = fields.Text()
    application_deadline = fields.Date()
    company_profile = fields.Text()
    student_ids = fields.Many2many(
        comodel_name="student.student",
        relation="company_student_rel",
        column1="company_id",
        column2="student_id",
    )
    average_package = fields.Char(help="Annual Package Offer")
    company_interview_date = fields.Date()
