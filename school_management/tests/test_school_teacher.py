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

    def test_check_sequence(self):
        """test case for teacher no #T00474"""
        self.assertNotEqual(
            self.school_teacher_01.teacher_no, False, "Teacher Number are not Generated"
        )

    def test_check_compute_method(self):
        """test cases for compute method  #T00474"""
        self.email_id = self.school_teacher_01.teacher_email
        self.assertEqual(
            self.email_id.endswith("@school.edu"),
            True,
            "Teacher E-mail ID not Generated Properly",
        )
        self.assertEqual(
            self.school_teacher_01.count_student,
            1,
            "Count of Total Student Number are not Matched",
        )

    def test_check_constrains(self):
        """test case for constrains validation  #T00474"""
        with self.assertRaises(ValidationError):
            self.env["school.teacher"].create(self.school_teacher_02)

    def test_check_unlink_method(self):
        """test cases for unlink method  #T00474"""
        self.school_teacher_03.unlink()
        self.check_record = self.env["school.teacher"].search_count(
            [("name", "like", "Shivangi Trivedi")]
        )
        self.assertEqual(self.check_record, 0, "Unlink Method are not Worked")
        with self.assertRaises(UserError):
            self.school_teacher_01.unlink()

    def test_check_name_get_method(self):
        """test case to test name_get method #T00474"""
        check = self.school_teacher_01.name_get()
        check = check[0]
        self.assertEqual(
            check[1],
            "Rimple Popat - [RIM]",
            "Not return name according name_get method",
        )
