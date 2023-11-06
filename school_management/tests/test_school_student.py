from datetime import date

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestSchoolStudent(TransactionCase):
    def setUp(self):
        super(TestSchoolStudent, self).setUp()
        # T00474 create config data
        self.res_config_data = self.env["res.config.settings"].create(
            {
                "minimum_student_age": 5,
                "maximum_teacher_age": 60,
                "fees_payment_time_limit": 2,
            }
        )

        # T00474 create student records
        self.school_student_01 = self.env["school.student"].create(
            {
                "name": "Rohan Movaliya",
                "division": "d",
                "standard": "std_9",
                "birth_date": "2004-05-06",
                "start_date": "2023-10-30",
                "total_girls": 50,
                "teacher_id": self.env.ref("school_management.teacher_record_01").id,
            }
        )
        self.school_student_02 = {
            "name": "Rohan Movaliya",
            "division": "b",
            "standard": "std_9",
            "mobile_no": "6767676746576574",
        }
        # T00474 create subject records
        self.school_subject_01 = self.env["school.subject"].create(
            {
                "subject_name": "Cyber Security",
                "subject_sort_name": "CS",
                "standard": "std_9",
            }
        )

    def test_01_check_sequence(self):
        # T00747 test case for student enrollment no
        self.assertNotEqual(
            self.school_student_01.enrollment_no, False, "Invalid Value"
        )

    def test_02_check_compute_method(self):
        #  T00474 test cases for compute methods
        self.assertEqual(self.school_student_01.age, 19, "Invalid Value")
        self.assertEqual(
            self.school_student_01.last_date, date(2023, 12, 30), "Invalid Value"
        )
        self.assertEqual(self.school_student_01.total_boys, 30, "Invalid Value")
        self.assertEqual(self.school_student_01.count_teacher, 1, "Invalid Value")
        self.assertEqual(self.school_student_01.count_subject, 1, "Invalid Value")

    def test_03_check_constrains(self):
        # T00474 test case for constrains validation
        with self.assertRaises(ValidationError):
            self.env["school.student"].create(self.school_student_02)

    def test_04_check_inverse_method(self):
        #  T00474 test case for inverse method
        self.school_student_01._inverse_total_no_of_boys()
        self.assertEqual(self.school_student_01.total_girls, 50, "Invalid Value")

    def test_05_check_server_action(self):
        # T00474 test case to server action
        self.school_student_01.set_blood_group()
        self.assertEqual(self.school_student_01.blood_group, "unkonwn", "Invalid Value")
