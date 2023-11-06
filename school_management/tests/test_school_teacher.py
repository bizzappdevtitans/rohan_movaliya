from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase


class TestSchoolTeacher(TransactionCase):
    def setUp(self):
        super(TestSchoolTeacher, self).setUp()
        # T00474  create teacher record
        self.school_teacher_01 = self.env["school.teacher"].create(
            {
                "name": "Rimple Popat",
                "sort_name": "RIM",
                "division": "d",
                "standard": "std_9",
            }
        )
        self.school_teacher_02 = {
            "name": "Rimple Popat",
            "sort_name": "RIM",
            "mobile_no": "46454548574657",
        }
        self.school_teacher_03 = self.env["school.teacher"].create(
            {
                "name": "Shivangi Trivedi",
                "sort_name": "SHT",
            }
        )
        self.school_student_01 = self.env["school.student"].create(
            {
                "name": "Rohan Movaliya",
                "division": "d",
                "standard": "std_9",
            }
        )

    def test_01_check_sequence(self):
        #  T00474 test case for teacher no
        self.assertNotEqual(self.school_teacher_01.teacher_no, False, "Invalid Value")

    def test_02_check_compute_method(self):
        # T00474 test cases for compute method
        self.email_id = self.school_teacher_01.teacher_email
        self.assertEqual(self.email_id.endswith("@school.edu"), True, "Invalid Value")
        self.assertEqual(self.school_teacher_01.count_student, 1, "Invalid Value")

    def test_03_check_constrains(self):
        # T00474 test case for constrains validation
        with self.assertRaises(ValidationError):
            self.env["school.teacher"].create(self.school_teacher_02)

    def test_04_check_unlink_method(self):
        # T00474 test cases for unlink method
        self.school_teacher_03.unlink()
        self.check_record = self.env["school.teacher"].search_count(
            [("name", "like", "Shivangi Trivedi")]
        )
        self.assertEqual(self.check_record, 0, "Invalid Value")
        with self.assertRaises(UserError):
            self.school_teacher_01.unlink()

    def test_05_check_name_get_method(self):
        # T00474 test case to test name_get method
        check = self.school_teacher_01.name_get()
        check = check[0]
        self.assertEqual(check[1], "Rimple Popat - [RIM]", "Invalid Value")
