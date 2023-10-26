from odoo import fields, models


class CompanyApplyWizard(models.TransientModel):
    _name = "company.apply.wizard"
    _description = "Company Apply Wizard"

    name = fields.Many2one(comodel_name="company.record")

    # NOTE : Need to improvement
    def action_confirm(self):
        pass
