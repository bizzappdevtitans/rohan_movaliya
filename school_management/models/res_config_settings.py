from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # T00337 added fields
    minimum_student_age = fields.Integer(
        config_parameter="school_management.minimum_student_age",
    )
    maximum_teacher_age = fields.Integer(
        config_parameter="school_management.maximum_teacher_age",
    )
    fees_payment_time_limit = fields.Integer(
        config_parameter="school_management.fees_payment_time_limit",
    )
