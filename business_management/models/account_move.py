from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"  # T00377 inherit object

    # T00377 added fields
    about_invoice = fields.Char()
