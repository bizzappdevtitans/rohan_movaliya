from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # T00468 addded fields
    year_of_graduation = fields.Char(
        default="2023-2024",
        config_parameter="placement_cell_management.year_of_graduation",
    )
