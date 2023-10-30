from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"  # T00391 inherit object

    # T00391 added fields
    about_delivery = fields.Text()
