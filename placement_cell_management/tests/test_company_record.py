from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestCompanyRecord(TransactionCase):
    def setUp(self):
        super(TestCompanyRecord, self).setUp()

    def test_01(self):
        company_record_01 = {
            "name": "Infosys",
            "address": "Ahmedabad",
            "contact": "6767676746576574",
        }

        with self.assertRaises(ValidationError):
            self.env["company.record"].create(company_record_01)
