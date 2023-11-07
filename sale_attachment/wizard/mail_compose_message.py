from odoo import models


class MailComposer(models.TransientModel):
    _inherit = "mail.compose.message"

    def _onchange_template_id(self, template_id, composition_mode, model, res_id):
        values = super(MailComposer, self)._onchange_template_id(
            template_id=template_id,
            composition_mode=composition_mode,
            model=model,
            res_id=res_id,
        )
        default_res_id = self._context.get("default_res_id")
        default_model = self._context.get("default_model")
        attachment_ids = (
            self.env["ir.attachment"]
            .search(
                [("res_id", "=", default_res_id), ("res_model", "=", default_model)]
            )
            .mapped("id")
        )
        attachment_ids.extend(values["value"].get("attachment_ids")[0][2])
        values["value"].update({"attachment_ids": [(6, 0, attachment_ids)]})
        return values
