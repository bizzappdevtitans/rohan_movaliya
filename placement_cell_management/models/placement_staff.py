from odoo import fields, models


class Placementstaff(models.Model):
    _name = "placement.staff"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Placement Staff"

    # T00468 added fields
    name = fields.Char(required=True)
    position = fields.Char()
    image = fields.Image()
    contact = fields.Char(string="Mobile", required=True)
    seating = fields.Char(required=True)
    email_id = fields.Char(string="E-mail")
