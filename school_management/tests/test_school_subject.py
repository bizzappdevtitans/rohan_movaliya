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

    def test_check_sequence(self):
        """test case for subject no  #T00474"""
        self.assertNotEqual(
            self.school_subject_01.subject_code,
            False,
            "Subject Code are not Generated Automatically",
        )

    def test_check_constrains(self):
        """test case for check subject sort name #T00474"""
        with self.assertRaises(ValidationError):
            self.env["school.subject"].create(self.school_subject_02)

    def test_check_name_get_method(self):
        """test case to test name_get method  #T00474"""
        check = self.school_subject_01.name_get()
        check = check[0]
        self.assertEqual(check[1], "ADA", "Not return name according name_get method")
