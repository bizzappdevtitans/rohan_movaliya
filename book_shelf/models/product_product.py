from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    # T00427 added fields
    book_short_name = fields.Char(string="Short Name")
    late_fee = fields.Float(string="Late Fees", default=10)
    is_issued = fields.Boolean(string="Is Issue", default=False)

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        """
        function which help to search product using other related field #T00427
        """
        args = args or []
        domain = []
        if name:
            domain = ["|", ("name", operator, name), ("categ_id", operator, name)]
        records = self.search(domain + args, limit=limit)
        return records.name_get()

    def name_get(self):
        """
        function to get name in a particular form #T00427
        """
        result = []
        for record in self:
            name = f"{record.name} - [{record.book_short_name}]"
            result.append((record.id, name))
        return result
