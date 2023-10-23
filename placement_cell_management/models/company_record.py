from odoo import fields, models


class ComapanyRecord(models.Model):
    _name = "company.record"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Comapny Records"

    # T00468 added field
    name = fields.Char(string="Company Name", required=True)
    image = fields.Image()
    address = fields.Char(string="Company Address")
    student_id = fields.Many2one(
        comodel_name="student.record", string="Student Details"
    )
    website = fields.Char()
    linkdin = fields.Char()
    hiring_position = fields.Char()
