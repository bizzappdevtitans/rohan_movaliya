# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class MailComposerMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    def _onchange_template_id(self, template_id, composition_mode, model, res_id):
        """Inherit method for attach chatter box document in email #T00456 """
        return super(MailComposerMessage, self)._onchange_template_id(
            template_id=template_id,
            composition_mode=composition_mode,
            model=model,
            res_id=res_id,
        )
