from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StudentRecords(models.Model):
    _name = "student.record"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Student Records"

    # T00468 added field
    name = fields.Char(tracking=True, required=True)
    image = fields.Image()
    enrollment_no = fields.Char(copy=False)
    gender = fields.Selection(
        selection=[("male", "Male"), ("female", "Female"), ("others", "Others")]
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
        ]
    )
    cpi = fields.Float(string="CPI")
    is_backlog = fields.Boolean(string="Backlog")
    no_of_backlog = fields.Integer(string="No of Backlog")
    email_id = fields.Char(string="E-mail")
    contact = fields.Char(string="Mobile")
    resume = fields.Binary()
    address = fields.Text(string="Student Address")
    skill = fields.Text(string="Technical Skill")
    achievement = fields.Text(string="Student Achievement")
    year = fields.Char(compute="_compute_year", readonly=True)
    company_id = fields.Many2one(comodel_name="company.record")
    company_ids = fields.Many2many(comodel_name="company.record")

    @api.constrains("cpi")
    def _check_cpi(self):
        """function to check value of CPT if input value is false the
        raise ValidationError #T00468
        """
        if self.cpi > 10 or self.cpi < 0:
            raise ValidationError(_("Invalid CPI\nPlease check it."))

    @api.model
    def _compute_year(self):
        self.year = self.env["ir.config_parameter"].get_param(
            "placement_cell_management.year"
        )

    def applied_company_details(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Company",
            "view_mode": "tree,form",
            "res_model": "company.record",
            "domain": [],
            "context": "{'create': False}",
        }
