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
    seating = fields.Char(required=True)
    email_id = fields.Char(string="E-mail")

    @api.constrains("contact")
    def _check_contact(self):
        """function to check contact no is valid or not otherwise show error #T00468"""
        contact = self.contact.replace(" ", "")
        if not (len(contact) == 10 and contact.isdigit()):
            raise ValidationError(_(f"Invalid Mobile Number '{self.contact}'"))
