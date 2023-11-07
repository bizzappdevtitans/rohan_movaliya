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

    def test_check_sequence(self):
        """test case for student enrollment no  #T00747"""
        self.assertNotEqual(
            self.school_student_01.enrollment_no,
            False,
            "Enrollment No are Not Generated",
        )

    def test_check_compute_method(self):
        """test cases for compute methods  #T00474"""
        self.assertEqual(self.school_student_01.age, 19, "Student age are Not Matched")
        self.assertEqual(
            self.school_student_01.last_date,
            date(2023, 12, 30),
            "Birth Date are Not Matched",
        )
        self.assertEqual(
            self.school_student_01.total_boys,
            30,
            "Count of total number of Boys are Wrong",
        )
        self.assertEqual(
            self.school_student_01.count_teacher, 1, "Count of Teacher number is Wrong"
        )
        self.assertEqual(
            self.school_student_01.count_subject, 1, "Count of Subject number is Wrong"
        )

    def test_check_constrains(self):
        """test case for constrains validation  #T00474"""
        with self.assertRaises(ValidationError):
            self.env["school.student"].create(self.school_student_02)

    def test_check_inverse_method(self):
        """test case for inverse method  #T00474"""
        self.school_student_01._inverse_total_no_of_boys()
        self.assertEqual(
            self.school_student_01.total_girls,
            50,
            "Count of total number of Girls are Wrong",
        )

    def test_check_server_action(self):
        """test case to server action #T00474"""
        self.school_student_01.set_blood_group()
        self.assertEqual(
            self.school_student_01.blood_group,
            "unkonwn",
            "Blood Group are Not Set Automatically",
        )
