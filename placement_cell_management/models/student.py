from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StudentStudent(models.Model):
    _name = "student.student"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Student Details"
    _rec_name = "name"

    # T00468 added field
    name = fields.Char(required=True)
    image = fields.Image()
    enrollment_no = fields.Char(copy=False, required=True)
    gender = fields.Selection(
        selection=[("male", "Male"), ("female", "Female"), ("others", "Others")],
        required=True,
    )
    department = fields.Selection(
        selection=[
            ("it", "Information Technology"),
            ("ce", "Computer Engineering"),
            ("chem", "Chemical Engineering"),
            ("mech", "Mechanical Engineering"),
            ("ee", "Electrical Engineering"),
            ("civil", "Civil Engineering"),
            ("aero", "Aerospace Engineering"),
        ],
        required=True,
    )
    cgpa = fields.Float(string="CGPA", required=True)
    is_backlog = fields.Boolean(string="Backlog")
    no_of_backlog = fields.Integer(string="No of Backlog")
    email_id = fields.Char(string="E-mail", required=True)
    contact = fields.Char(string="Mobile", required=True)
    resume = fields.Binary()
    address = fields.Text(string="Student Address")
    academic_records = fields.Text()
    training_attendance = fields.Float(required=True)
    skill = fields.Text(string="Technical Skill")
    achievement = fields.Text(string="Student Achievement")
    year_of_graduation = fields.Char(compute="_compute_year", readonly=True)
    company_ids = fields.Many2many(
        comodel_name="company.company",
        relation="company_student_rel",
        column1="student_id",
        column2="company_id",
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("applied", "Applied"),
            ("blocked", "Blocked"),
            ("placed", "Placed"),
        ],
        string="Status",
        default="draft",
        readonly=True,
    )

    @api.constrains("cgpa", "training_attendance")
    def _check_cpi(self):
        """function to check value of CGPA and training attendance if input value is false the
        raise ValidationError #T00468
        """
        if self.cgpa > 10 or self.cgpa < 0:
            raise ValidationError(_(f"Invalid Value of CGPA ({self.cgpa})"))
        if self.training_attendance > 100 or self.training_attendance < 0:
            raise ValidationError(
                _(f"Invalid Value of Attendance ({self.training_attendance})")
            )

    @api.model
    def _compute_year(self):
        """function to get value from configuration #T00468"""
        self.year_of_graduation = self.env["ir.config_parameter"].get_param(
            "placement_cell_management.year_of_graduation"
        )

    @api.constrains("cgpa", "training_attendance")
    def _check_eligibility_criteria(self):
        """function to check eligibility criteria to according to collage
        rules #T00468
        """
        # get minimum attendance value from config setting
        attendence = float(
            self.env["ir.config_parameter"].get_param(
                "placement_cell_management.attendance"
            )
        )
        # get minimum cgpa value from config setting
        cgpa = float(
            self.env["ir.config_parameter"].get_param("placement_cell_management.cgpa")
        )
        if self.cgpa < cgpa or self.training_attendance < attendence:
            self.state = "blocked"

    @api.model
    def action_send_email_for_training(self):
        """method to send mail for inform training session #T00468"""
        mail_template = self.env.ref(
            "placement_cell_management.tarining_schedule_template"
        )
        mail_template.send_mail(self.id, force_send=True)

    @api.model
    def action_send_email_for_placement(self):
        """method to send mail for inform company come for placement #T00468"""
        mail_template = self.env.ref(
            "placement_cell_management.interview_schedule_template"
        )
        mail_template.send_mail(self.id, force_send=True)

    @api.constrains("contact")
    def _check_contact(self):
        """function to check contact no is valid or not otherwise show error #T00468"""
        contact = self.contact.replace(" ", "")
        if not (len(contact) == 10 and contact.isdigit()):
            raise ValidationError(_(f"Invalid Mobile Number ({self.contact})"))
