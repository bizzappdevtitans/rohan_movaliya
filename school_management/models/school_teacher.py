from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "School Teachers"

    @api.model
    def default_get(self, fields):
        """function to set default email id when user create a new record #T00337"""
        record = super(SchoolTeacher, self).default_get(fields)
        record.update({"teacher_email": "nameteacher_no@school.edu"})
        return record

    # T00337 added fields
    teacher_no = fields.Char(
        string="Teacher No.",
        required=True,
        readonly=True,
        default=lambda self: _("Teacher No"),
    )
    name = fields.Char(required=True)
    sort_name = fields.Char(string="Sort Code", copy=False)
    age = fields.Integer(string="Teacher Age")
    qualification = fields.Char(string="Qualification of Teacher")
    about_teacher = fields.Html(string="About Teacher Background")
    mobile_no = fields.Char(string="Teacher Mobile No")
    standard = fields.Selection(
        selection=[
            ("std_9", "9"),
            ("std_10", "10"),
            ("std_11", "11"),
            ("std_12", "12"),
        ],
        help="Which Standard of Class Teacher",
    )
    division = fields.Selection(
        selection=[
            ("a", "A"),
            ("b", "B"),
            ("c", "C"),
            ("d", "D"),
            ("e", "E"),
        ],
        help="Which Division of Class Teacher",
    )
    teacher_email = fields.Char(
        string="Teacher Email_id",
        compute="_compute_mail_id",
    )
    subject_ids = fields.Many2many(comodel_name="school.subject", string="Subjects")
    color = fields.Integer()

    # T00337 added fields for smart buttons
    count_student = fields.Integer(
        string="Count Students", compute="_compute_count_student"
    )

    @api.model
    def create(self, vals):
        """function to generate unique enrollment number for each new records #T00337"""
        vals["teacher_no"] = self.env["ir.sequence"].next_by_code("school.teacher")
        return super(SchoolTeacher, self).create(vals)

    @api.model
    def _compute_mail_id(self):
        """Create teacher email id using name and  id of teacher #T00337"""
        if self.name and self.teacher_no:
            name = self.name
            name = name.replace(" ", "").lower()
            number = self.teacher_no
            number = number[3:]
            email = f"{name}{number}@school.edu"
        self.teacher_email = email

    @api.depends("standard", "division")
    def _compute_count_student(self):
        """count a student no. #T00337"""
        for record in self:
            record.count_student = self.env["school.student"].search_count(
                [("standard", "=", self.standard), ("division", "=", self.division)]
            )

    def view_student_ids(self):
        """get students records #T00337"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Students",
            "view_mode": "tree,form",
            "res_model": "school.student",
            "domain": [
                ("standard", "=", self.standard),
                ("division", "=", self.division),
            ],
            "context": "{'create': False}",
        }

    def name_get(self):
        """function to get teacher name and sort code together #T00337"""
        teacher_list = []
        for record in self:
            name = f"{record.name} - [{record.sort_name}]"
            teacher_list.append((record.id, name))
        return teacher_list

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        """function to user search any particular relational
        fields using other fields #T00337"""
        args = args or []
        if name:
            record = self.search(
                [
                    "|",
                    "|",
                    "|",
                    "|",
                    ("name", operator, name),
                    ("teacher_no", operator, name),
                    ("sort_name", operator, name),
                    ("division", operator, name),
                    ("standard", operator, name),
                ]
            )
            return record.name_get()
        return self.search([("name", operator, name)] + args, limit=limit).name_get()

    @api.constrains("mobile_no")
    def _check_mobile_no(self):
        """function to check mobile no is valid or not otherwise show error #T00337"""
        contact = self.mobile_no.replace(" ", "")
        if not (len(contact) == 10 and contact.isdigit()):
            raise ValidationError(_("Invalid Mobile Number"))

    def unlink(self):
        """User cannot delete a record of teacher which
        is class teacher of any class #T00337"""
        if self.division and self.standard:
            raise UserError(_("Class Teacher record are not deleted"))
        return super(SchoolTeacher, self).unlink()
