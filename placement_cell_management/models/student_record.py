from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StudentRecords(models.Model):
    _name = "student.record"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Student Records"
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
            ("it", "Information Techonology"),
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

    @api.constrains("cgpa", "training_attendance")
    def _check_cpi(self):
        """function to check value of CGPA and training attendance if input value is false the
        raise ValidationError #T00468
        """
        if self.cgpa > 10 or self.cgpa < 0:
            raise ValidationError(_("Invalid CGPA\nPlease check it."))
        if self.training_attendance > 100 or self.training_attendance < 0:
            raise ValidationError(_("Invalid Attendence\nPlease check it."))

    @api.model
    def _compute_year(self):
        """function to get value from ci=onfiguration #T00468"""
        self.year_of_graduation = self.env["ir.config_parameter"].get_param(
            "placement_cell_management.year_of_graduation"
        )

    @api.constrains("cgpa", "training_attendance")
    def _check_eligibility_criteria(self):
        """function to check eligiblity crieteria to according to collage
        rules #T00468
        """
        # get minimum attendence value from config setting
        attendence = float(
            self.env["ir.config_parameter"].get_param(
                "placement_cell_management.attendence"
            )
        )
        # get minimum cgpa value from config setting
        cgpa = float(
            self.env["ir.config_parameter"].get_param("placement_cell_management.cgpa")
        )
        if self.cgpa < cgpa or self.training_attendance < attendence:
            self.state = "rejected"

    @api.constrains("contact")
    def _check_mobile_no(self):
        """function to check mobile no is valid or not otherwise show error #T00468"""
        if self.contact and len(self.contact.replace(" ", "")) != 10:
            raise ValidationError(_("Invalid Contact Number"))

    def action_send_email_for_training(self):
        """method to send mail for inform training session #T00468"""
        mail_template = self.env.ref(
            "placement_cell_management.tarining_schedule_template"
        )
        mail_template.send_mail(self.id, force_send=True)

    def action_send_email_for_placement(self):
        """method to send mail for inform company driven for placement #T00468"""
        mail_template = self.env.ref(
            "placement_cell_management.company_driven_schedule_template"
        )
        mail_template.send_mail(self.id, force_send=True)
