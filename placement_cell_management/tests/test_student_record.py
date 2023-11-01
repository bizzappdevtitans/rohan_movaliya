from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestStudentRecord(TransactionCase):
    def setUp(self):
        super(TestStudentRecord, self).setUp()
        self.student_record_01 = self.env["student.student"].create(
            {
                "name": "Harpal Nasid",
                "enrollment_no": "2102031000127",
                "gender": "female",
                "department": "ce",
                "cgpa": "6.00",
                "training_attendance": "92.09",
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
            }
        )

    def test_01(self):
        self.assertEqual(self.student_record_01.state, "blocked", "Invalid State")

    def test_02(self):
        self.student_record_02.action_send_email_for_training()
        self.student_record_02.action_send_email_for_placement()

    def test_03(self):
        student_record = {
            "name": "Rohan Movaliya",
            "enrollment_no": "2102031000126",
            "gender": "male",
            "department": "it",
            "cgpa": "60.00",
            "training_attendance": "92.09",
        }

        with self.assertRaises(ValidationError):
            self.env["student.student"].create(student_record)

    def test_04(self):
        student_record = {
            "name": "Rohan Movaliya",
            "enrollment_no": "2102031000126",
            "gender": "male",
            "department": "it",
            "cgpa": "7.44",
            "training_attendance": "110.12",
        }

        with self.assertRaises(ValidationError):
            self.env["student.student"].create(student_record)

    def test_05(self):
        student_record = {
            "name": "Rohan Movaliya",
            "enrollment_no": "2102031000126",
            "gender": "male",
            "department": "it",
            "cgpa": "7.00",
            "training_attendance": "92.09",
            "contact": "6767676746576574",
        }

        with self.assertRaises(ValidationError):
            self.env["student.student"].create(student_record)

    def test_06(self):
        self.assertEqual(
            self.student_record_01.year_of_graduation, "2023-2024", "Invalid Value"
        )
