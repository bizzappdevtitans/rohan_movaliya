from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"  # T00399 inherit object

    # T00399 added fields
    about_purchase = fields.Text()
