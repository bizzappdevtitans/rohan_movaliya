from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class Placementstaff(models.Model):
    _name = "placement.staff"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Placement Staff"

    # T00468 added fields
    name = fields.Char(required=True)
    position = fields.Char()
    image = fields.Image()
    contact = fields.Char(string="Mobile", required=True)
    seatting = fields.Char(required=True)

    @api.constrains("contact")
    def _check_mobile_no(self):
        """function to check mobile no is valid or not, otherwise show error #T00468"""
        if self.contact and len(self.contact.replace(" ", "")) != 10:
            raise ValidationError(_("Invalid Contact Number"))
