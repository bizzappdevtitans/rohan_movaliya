# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolStudent(models.Model):
    _name = "school.student"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "School Students"
    _rec_name = "name"

    @api.model
    def default_get(self, fields):
        """function to set value of fees when user create a new record #T00337"""
        record = super(SchoolStudent, self).default_get(fields)
        record.update({"total_fees": 35700})
        return record

    # T00337 added fields
    enrollment_no = fields.Char(
        string="No",
        required=True,
        readonly=True,
        default=lambda self: _("Enrollment No"),
    )
    name = fields.Char(string="Student Name", required=True)
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female"), ("others", "Others")],
        string="Student Gender",
    )
    birth_date = fields.Date(string="Student Birth Date")
    age = fields.Integer(string="Student Age", compute="_compute_age", store=True)
    blood_group = fields.Selection(
        selection=[
            ("unkonwn", "Unknown"),
            ("A+", "A+ve"),
            ("B+", "B+ve"),
            ("O+", "O+ve"),
            ("AB+", "AB+ve"),
        ],
        string="Student Blood Group",
    )
    mobile_no = fields.Char(string="Parents Mobile No.")
    standard = fields.Selection(
        selection=[
            ("std_9", "9"),
            ("std_10", "10"),
            ("std_11", "11"),
            ("std_12", "12"),
        ],
        string="Student Standard",
        required=True,
    )
    division = fields.Selection(
        selection=[
            ("a", "A"),
            ("b", "B"),
            ("c", "C"),
            ("d", "D"),
            ("e", "E"),
        ],
        string="Student Division",
        required=True,
        tracking=True,
    )
    # T00337 added fields for use Monetary fields
    company_id = fields.Many2one(
        comodel_name="res.company",
        store=True,
        copy=False,
        string="Company",
        default=lambda self: self.env.user.company_id.id,
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="company_id.currency_id",
    )
    total_fees = fields.Monetary(string="Fees")
    start_date = fields.Date(
        string="Payment Start Date", default=date.today(), tracking=True
    )
    last_date = fields.Date(string="Payment Last Date", compute="_compute_last_date")
    teacher_id = fields.Many2one(
        comodel_name="school.teacher",
        string="Class Teacher",
        domain="[('standard', '=', standard), ('division', '=', division),]",
    )
    color = fields.Integer()
    # T00337 added field for smart button
    count_teacher = fields.Integer(
        string="Count Teacher No", compute="_compute_count_teacher"
    )
    count_subject = fields.Integer(
        string="Count Subject No", compute="_compute_count_subject"
    )

    # T00433 added fields
    total_boys = fields.Integer(
        string="Total No. of Boys",
        compute="_compute_no_of_boys",
        inverse="_inverse_total_no_of_boys",
    )
    total_girls = fields.Integer(string="Total No. of Girls")

    @api.model
    def create(self, vals):
        """function to generate unique enrollment number for each new records #T00337"""
        vals["enrollment_no"] = self.env["ir.sequence"].next_by_code("school.student")
        return super(SchoolStudent, self).create(vals)

    @api.depends("teacher_id")
    def _compute_count_teacher(self):
        """function to count No. of class teacher #T00337"""
        for record in self:
            record.count_teacher = len(self.teacher_id)

    @api.depends("standard")
    def _compute_count_subject(self):
        """function to count No. of subject #T00337"""
        for record in self:
            record.count_subject = self.env["school.subject"].search_count(
                [("standard", "=", self.standard)]
            )

    def view_teacher_ids(self):
        """function to show class teacher records #T00337"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Class Teacher",
            "view_mode": "tree,form",
            "res_model": "school.teacher",
            "domain": [
                ("division", "=", self.division),
                ("standard", "=", self.standard),
            ],
            "context": "{'create': False}",
        }

    def view_subject_ids(self):
        """function to show subject records #T00337"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Class Subject",
            "view_mode": "tree,form",
            "res_model": "school.subject",
            "domain": [("standard", "=", self.standard)],
            "context": "{'create': False}",
        }

    @api.depends("birth_date")
    def _compute_age(self):
        """function to calculate age using birth date #T00337"""
        self.age = False
        for rec in self:
            rec.age = relativedelta(date.today(), rec.birth_date).years

    @api.depends("start_date")
    def _compute_last_date(self):
        """function to calculate last date to pay fees #T00337"""
        self.last_date = date.today()
        # get limit to pay fees in the settings
        limit = int(
            self.env["ir.config_parameter"].get_param(
                "school_management.fees_payment_time_limit"
            )
        )
        if self.start_date:
            for record in self:
                record.last_date = self.start_date + relativedelta(months=+limit)

    @api.constrains("mobile_no")
    def _check_mobile_no(self):
        """function to check mobile no is valid or not otherwise show error #T00337"""
        if self.mobile_no and len(self.mobile_no.replace(" ", "")) != 10:
            raise ValidationError(_("Invalid Mobile Number"))

    def set_blood_group(self):
        """function to set blood group is unknown #T00415"""
        if not self.blood_group:
            self.blood_group = "unkonwn"

    def delete_records(self):
        """function which run scheduled time #T00432"""
        student_record = self.search([])
        return student_record.unlink()

    @api.depends("total_girls")
    def _compute_no_of_boys(self):
        for record in self:
            record.total_boys = 80 - record.total_girls

    def _inverse_total_no_of_boys(self):
        for record in self:
            record.total_girls = 80 - record.total_boys
