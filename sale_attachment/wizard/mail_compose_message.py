from odoo import api, fields, models


class MailComposer(models.TransientModel):
    _inherit = "mail.compose.message"

    # T00456 added field
    is_attach = fields.Boolean(help="attach all chatter attachments in mail")

    @api.onchange("is_attach")
    def add_extra_attachments(self):
        """method for attach chatter attachment in e-mail #T00456"""
        chatter_attachment = (
            self.env["ir.attachment"]
            .search(
                [
                    ("res_id", "=", self.env.context.get("active_id")),
                    ("res_model", "=", "sale.order"),
                ]
            )
            .mapped("id")
        )
        if not self.is_attach:
            for attachment in chatter_attachment:
                self.update({"attachment_ids": [(3, attachment, 0)]})
        else:
            for attachment in chatter_attachment:
                self.update({"attachment_ids": [(4, attachment)]})
