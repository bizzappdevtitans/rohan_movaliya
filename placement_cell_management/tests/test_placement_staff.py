from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestPlacementStaff(TransactionCase):
    def setUp(self):
        super(TestPlacementStaff, self).setUp()
        self.staff_record_01 = {
            "name": "Ms. Bhoomi Parmar",
            "seating": "Ahmedabad",
            "contact": "6767676746576574",
        }

    def test_01_to_check_constrains(self):
        """function fot test constrains  #T004689"""
        with self.assertRaises(ValidationError):
            self.env["placement.staff"].create(self.staff_record_01)
