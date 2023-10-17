from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # T00427 added fields
    min_day = fields.Integer(
        string="Minimum Day",
        default=5,
        config_parameter="book_shelf.min_day",
    )
    max_day = fields.Integer(
        string="Maximum Day ",
        default=15,
        config_parameter="book_shelf.max_day",
    )
