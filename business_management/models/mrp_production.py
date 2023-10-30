from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"  # T00409 inherit object

    # T00409 added fields
    about_manufacturing = fields.Text()
