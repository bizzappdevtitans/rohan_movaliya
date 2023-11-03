from odoo import _, fields, models
from odoo.exceptions import ValidationError


class CompanyApplyWizard(models.TransientModel):
    _name = "company.apply.wizard"
    _description = "Company Apply Wizard"

    companies_id = fields.Many2one(
        comodel_name="company.company",
        string="Company",
    )

    def action_confirm(self):
        """button to apply for company placements #T00468"""
        student = self.env["student.student"].browse(self._context.get("active_id"))
        if not len(student.company_ids) >= 3:
            selected_companies = self.companies_id
            student.company_ids = [(4, company.id) for company in selected_companies]
            student.write({"state": "applied"})
            return {"type": "ir.actions.act_window_close"}
        else:
            raise ValidationError(_("You cannot apply more than 3 Companies"))
