# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # T00337 added fields
    minimum_student_age = fields.Integer(
        string="Minimum student age",
        default=5,
        config_parameter="school_management.minimum_student_age",
    )
    maximum_teacher_age = fields.Integer(
        string="maximum teacher age",
        default=60,
        config_parameter="school_management.maximum_teacher_age",
    )
    fees_payment_time_limit = fields.Integer(
        string="fees payment limit",
        default=2,
        config_parameter="school_management.fees_payment_time_limit",
    )
