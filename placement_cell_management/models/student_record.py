from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StudentRecords(models.Model):
    _name = "student.record"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Student Records"
    _rec_name = "name"

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
    cgpa = fields.Float(string="CGPA")
    is_backlog = fields.Boolean(string="Backlog")
    no_of_backlog = fields.Integer(string="No of Backlog")
    email_id = fields.Char(string="E-mail")
    contact = fields.Char(string="Mobile")
    resume = fields.Binary()
    address = fields.Text(string="Student Address")
    academic_records = fields.Text()
    training_attendance = fields.Float()
    skill = fields.Text(string="Technical Skill")
    achievement = fields.Text(string="Student Achievement")
    year_of_graduation = fields.Char(compute="_compute_year", readonly=True)
    company_ids = fields.Many2many(comodel_name="company.record")
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("applied", "Applied"),
            ("shortlisted", "Shortlisted"),
            ("rejected", "Rejected"),
            ("placed", "Placed"),
        ],
        string="Status",
        default="draft",
        readonly=True,
    )

    @api.constrains("cpi")
    def _check_cpi(self):
        """function to check value of CGPA if input value is false the
        raise ValidationError #T00468
        """
        if self.cpi > 10 or self.cpi < 0:
            raise ValidationError(_("Invalid CPI\nPlease check it."))

    @api.model
    def _compute_year(self):
        """function to get value from ci=onfiguration #T00468"""
        self.year_of_graduation = self.env["ir.config_parameter"].get_param(
            "placement_cell_management.year_of_graduation"
        )

    def applied_company_details(self):
        """Smart button to show company records #T00468"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Company",
            "view_mode": "tree,form",
            "res_model": "company.record",
            "domain": [],
            "context": "{'create': False}",
        }

    @api.onchange("company_ids")
    def action_draft(self):
        if len(self.company_ids) == 0 and self.training_attendance > 90.00:
            self.state = "draft"

    @api.onchange("company_ids")
    def action_applied(self):
        if len(self.company_ids) > 0 and self.training_attendance > 90.00:
            self.state = "applied"

    @api.onchange("training_attendance")
    def action_rejected(self):
        if self.training_attendance < 90.00:
            self.state = "rejected"

    #  NOTE : Need to improvement #T00468
    # def send_training_email(self, student, training):
    #     email_template = self.env.ref("placement_cell.training_email_template")
    #     email_values = {
    #         "student_name": student.name,
    #         "training_name": training.name,
    #         "training_date": training.date,
    #         "training_venue": training.venue,
    #     }
    #     email = email_template.send_mail(
    #         student.id, force_send=True, email_values=email_values
    #     )

    @api.onchange("company_ids")
    def _onchange_company(self):
        """function to check limit to applly for complany #T00468"""
        if len(self.company_ids) >= 4:
            raise ValidationError(_("You can apply only 3 companies"))

    def action_send_email(self):
        """method for run server actions #T00468"""
        mail_template = self.env.ref(
            "placement_cell_management.tarining_schedule_template"
        )
        mail_template.send_mail(self.id, force_send=True)
