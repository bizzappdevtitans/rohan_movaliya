from odoo import fields, models


class ComapanyRecord(models.Model):
    _name = "company.record"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Comapny Records"

    # T00468 added field
    name = fields.Char(string="Company Name")
    address = fields.Char(string="Company Address")
