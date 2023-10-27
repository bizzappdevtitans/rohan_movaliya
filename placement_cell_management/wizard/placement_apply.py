from odoo import _, fields, models
from odoo.exceptions import ValidationError


class CompanyApplyWizard(models.TransientModel):
    _name = "company.apply.wizard"
    _description = "Company Apply Wizard"

    name_id = fields.Many2one(comodel_name="company.record")

    def action_confirm(self):
        student = self.env["student.record"].browse(self._context.get("active_id"))
        if not len(student.company_ids) >= 3:
            selected_companies = self.name_id
            student.company_ids = [(4, company.id) for company in selected_companies]
            student.write({"state": "applied"})
            return {"type": "ir.actions.act_window_close"}
        else:
            raise ValidationError(_("You cannot apply more than 3 Companies"))
