from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestStudentStudent(TransactionCase):
    def setUp(self):
        super(TestStudentStudent, self).setUp()
        #  create system parameter record #T00468
        self.res_config_data = self.env["res.config.settings"].create(
            {"year_of_graduation": "2023 - 2024", "cgpa": 8.0, "attendence": 90.00}
        )

        self.student_record_01 = self.env["student.student"].create(
            {
                "name": "Harpal Nasid",
                "enrollment_no": "2102031000127",
                "gender": "female",
                "department": "ce",
                "cgpa": "6.00",
                "training_attendance": "92.09",
                "email_id": "rohanmovaliya55@gmail.com",
                "contact": "99874 74884",
            }
        )
        self.student_record_02 = self.env["student.student"].create(
            {
                "name": "Rohan Movaliya",
                "enrollment_no": "2102031000126",
                "gender": "male",
                "department": "it",
                "cgpa": "9.99",
                "training_attendance": "92.09",
                "email_id": "rohanmovaliya55@gmail.com",
                "contact": "99874 74884",
            }
        )
        self.student_record_03 = {
            "name": "Rohan Movaliya",
            "enrollment_no": "2102031000126",
            "gender": "male",
            "department": "it",
            "cgpa": "60.00",
            "training_attendance": "92.09",
            "email_id": "rohanmovaliya55@gmail.com",
            "contact": "99874 74884",
        }

        self.student_record_04 = {
            "name": "Rohan Movaliya",
            "enrollment_no": "2102031000126",
            "gender": "male",
            "department": "it",
            "cgpa": "7.44",
            "training_attendance": "110.12",
            "email_id": "rohanmovaliya55@gmail.com",
            "contact": "99874 74884",
        }

        self.student_record_05 = {
            "name": "Rohan Movaliya",
            "enrollment_no": "2102031000126",
            "gender": "male",
            "department": "it",
            "cgpa": "7.00",
            "training_attendance": "92.09",
            "contact": "6767676746576574",
            "email_id": "rohanmovaliya55@gmail.com",
        }

    def test_01_to_check_changes_state(self):
        """test case for state changes #T00468"""
        self.assertEqual(self.student_record_01.state, "blocked", "Invalid state")

    def test_02_to_check_server_action(self):
        """test cases for server actions #T00468"""
        self.student_record_02.action_send_email_for_training()
        self.student_record_02.action_send_email_for_placement()

    def test_03_to_check_constrains(self):
        """test case for raise validation error #T00468"""
        with self.assertRaises(ValidationError):
            self.env["student.student"].create(self.student_record_03)

        with self.assertRaises(ValidationError):
            self.env["student.student"].create(self.student_record_04)

        with self.assertRaises(ValidationError):
            self.env["student.student"].create(self.student_record_05)

    def test_04_to_check_config_parameter(self):
        """test cases for check compute fields value #T00468"""
        self.assertEqual(
            self.student_record_01.year_of_graduation, "2023-2024", "Invalid Value"
        )
