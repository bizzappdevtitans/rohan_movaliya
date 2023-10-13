# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command, models


class MailComposerMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def _onchange_template_id(self, template_id, composition_mode, model, res_id):
        if template_id:
            values = self.generate_email_for_composer(
                template_id,
                [res_id],
                [
                    "subject",
                    "body_html",
                    "email_from",
                    "email_to",
                    "partner_to",
                    "email_cc",
                    "reply_to",
                    "attachment_ids",
                    "mail_server_id",
                ],
            )[res_id]

            attachment_ids = []
            Attachment = self.env["ir.attachment"]
            attach = self.env["mail.message"]
            for attach_fname, attach_datas in values.pop("attachments", []):
                data_attach = {
                    "name": attach_fname,
                    "datas": attach_datas,
                    "res_model": "mail.compose.message",
                    "res_id": 0,
                    "type": "binary",
                }

                attachment_ids.append(Attachment.create(data_attach).id)
                attachment_ids.append(attach.attachment_ids.id)

            if values.get("attachment_ids", []) or attachment_ids:
                values["attachment_ids"] = [
                    Command.set(values.get("attachment_ids", []) + attachment_ids)
                ]

        return {"value": values}
