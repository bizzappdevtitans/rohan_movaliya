from odoo import fields, models


class ComapanyRecord(models.Model):
    _name = "company.record"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Comapny Records"

    # T00468 added field
    name = fields.Char(string="Company Name", required=True)
    image = fields.Image()
    address = fields.Text(string="Company Address")
    website = fields.Char()
    linkedin = fields.Char()
    job_position = fields.Text()
    job_description = fields.Text()
    contact = fields.Char()
    application_deadline = fields.Date()
    company_profile = fields.Text()
    student_ids = fields.Many2many(comodel_name="student.record")
    package_offer = fields.Char()
