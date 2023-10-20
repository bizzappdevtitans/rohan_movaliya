from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StudentRecords(models.Model):
    _name = "student.record"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Student Records"

    # added field
    name = fields.Char(string="Student Name", required=True, tracking=True)
    image = fields.Image(string="Student Image")
    enrollment_no = fields.Char(string="Enrollment Number", required=True, copy=False)
    gender = fields.Selection(
        selection=[("male", "Male"), ("female", "Female"), ("others", "Others")],
        string="Student Gender",
        required=True,
    )
    department = fields.Selection(
        selection=[
            ("it", "Information Techonology"),
            ("ce", "Computer Engineering"),
            ("chem", "Chemical Engineering"),
            ("mech", "Mechanical Engineering"),
            ("ee", "Electrical Engineering"),
            ("civil", "Civil Engineering"),
            ("aero", "Aerospace Engineering"),
        ],
        string=" Student Department",
        required=True,
    )
    cpi = fields.Float(string="CPI")
    is_backlog = fields.Boolean(string="Backlog")
    no_of_backlog = fields.Integer(string="No of Backlog")

    @api.constrains("cpi")
    def _check_cpi(self):
        """function to check value of CPT if input value is false the
        raise ValidationError"""
        if self.cpi > 10 or self.cpi < 0:
            raise ValidationError(_("Invalid CPI\nPlease check it."))
