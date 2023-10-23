from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    year = fields.Char(
        string="Placement Year",
        default=2023 - 2024,
        config_parameter="placement_cell_management.year",
    )
