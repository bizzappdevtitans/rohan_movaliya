from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestSchoolSubject(TransactionCase):
    def setUp(self):
        super(TestSchoolSubject, self).setUp()
        # T00474 create subject record
        self.school_subject_01 = self.env["school.subject"].create(
            {
                "subject_name": "Analysis and Design of Algorithm",
                "subject_sort_name": "ADA",
                "standard": "std_9",
            }
        )
        self.school_subject_02 = {
            "subject_name": "Aptitude Building and Professional Skills",
            "subject_sort_name": "ABPS - I",
            "standard": "std_9",
        }

    def test_01_check_sequence(self):
        # T00474 test case for subject no
        self.assertNotEqual(self.school_subject_01.subject_code, False, "Invalid Value")

    def test_02_check_constrains(self):
        # T00474 test case for check subject sort name
        with self.assertRaises(ValidationError):
            self.env["school.subject"].create(self.school_subject_02)

    def test_03_check_name_get_method(self):
        # T00474 test case to test name_get method
        check = self.school_subject_01.name_get()
        check = check[0]
        self.assertEqual(check[1], "ADA", "Invalid Value")
