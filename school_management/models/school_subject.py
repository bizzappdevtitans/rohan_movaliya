from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SchoolSubject(models.Model):
    _name = "school.subject"
    _description = "School Subjects"

    # T00337 added fields
    subject_code = fields.Char(
        readonly=True,
        required=True,
        default=lambda self: _("Subject Code"),
    )
    subject_name = fields.Char()
    subject_sort_name = fields.Char()
    standard = fields.Selection(
        selection=[
            ("std_9", "9"),
            ("std_10", "10"),
            ("std_11", "11"),
            ("std_12", "12"),
        ],
        required=True,
    )
    teacher_ids = fields.Many2many(comodel_name="school.teacher", string="Trachers")
    color = fields.Integer()

    @api.model
    def create(self, vals):
        vals["subject_code"] = self.env["ir.sequence"].next_by_code("school.subject")
        return super(SchoolSubject, self).create(vals)

    def name_get(self):
        """function to get subject short name #T00337"""
        subject_list = []
        for record in self:
            name = f"{record.subject_sort_name}"
            subject_list.append((record.id, name))
        return subject_list

    @api.constrains("subject_sort_name")
    def _check_sort_name(self):
        """function to check subject sort name is valid or
        not otherwise show error #T00337"""
        if self.subject_sort_name and len(self.subject_sort_name) > 5:
            raise ValidationError(
                _("Subject Sort Name size is Maximum 4 characters allowed!")
            )
