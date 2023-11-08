from odoo import models


class MailComposer(models.TransientModel):
    _inherit = "mail.compose.message"

    def _onchange_template_id(self, template_id, composition_mode, model, res_id):
        """inherited method to add attachment in email #T00456"""
        values = super(MailComposer, self)._onchange_template_id(
            template_id=template_id,
            composition_mode=composition_mode,
            model=model,
            res_id=res_id,
        )
        default_res_id = self._context.get("default_res_id")
        attachment_ids = (
            self.env["ir.attachment"]
            .search([("res_id", "=", default_res_id), ("res_model", "=", "sale.order")])
            .mapped("id")
        )
        default_attachment = values["value"].get("attachment_ids")[0][2]
        attachment_ids.extend(default_attachment)
        values["value"].update({"attachment_ids": [(6, 0, attachment_ids)]})
        return values
