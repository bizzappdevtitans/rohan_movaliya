from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"  # T00411 inherit object

    # T00411 added fields
    about_project = fields.Text()
