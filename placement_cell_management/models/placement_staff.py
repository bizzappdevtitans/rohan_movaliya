from odoo import fields, models


class Placementstaff(models.Model):
    _name = "placement.staff"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Placement Staff"

    name = fields.Char()
    position = fields.Char()
    image = fields.Image()
    contact = fields.Char(string="Mobile")
    seatting = fields.Char()
