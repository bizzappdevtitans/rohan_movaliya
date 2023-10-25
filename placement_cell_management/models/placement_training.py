from odoo import fields, models


class PlacementTraining(models.Model):
    _name = "placement.training"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Placement Training"

    # T00468 added field
    name = fields.Char(string="Company Name")
