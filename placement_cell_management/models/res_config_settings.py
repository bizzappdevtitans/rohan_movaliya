from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # T00468 addded fields
    year_of_graduation = fields.Char(
        config_parameter="placement_cell_management.year_of_graduation",
    )
    attendence = fields.Float(config_parameter="placement_cell_management.attendence")
    cgpa = fields.Float(config_parameter="placement_cell_management.cgpa")
