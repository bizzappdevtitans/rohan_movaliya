from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestPlacementStaff(TransactionCase):
    def setUp(self):
        super(TestPlacementStaff, self).setUp()

    def test_01(self):
        staff_record_01 = {
            "name": "Ms. Bhoomi Parmar",
            "seating": "Ahmedabad",
            "contact": "6767676746576574",
        }

        with self.assertRaises(ValidationError):
            self.env["placement.staff"].create(staff_record_01)
