from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"  # T00411 inherit object

    # T00411 added fields
    about_task = fields.Text()
