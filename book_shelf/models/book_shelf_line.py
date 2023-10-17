from datetime import date

from odoo import api, fields, models


class BookShelfLine(models.Model):
    _name = "book.shelf.line"
    _description = "Book Shelf Line"
    _rec_name = "product_id"

    # T00427 added fields
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Book Product",
        domain=[("categ_id", "=", "Books"), ("is_issued", "=", False)],
    )
    max_day = fields.Integer(string="Maximum Days")
    min_day = fields.Integer(string="Minimum Days")
    issue_date = fields.Date(string="Date", default=date.today())
    late_fee = fields.Float(string="Fee", compute="_compute_late_fee", store=True)
    shelf_id = fields.Many2one(comodel_name="book.shelf", string="Book Shelf")

    @api.depends("product_id")
    def _compute_late_fee(self):
        """
        function to get a value from product #T00427
        """
        for line in self:
            line.late_fee = line.product_id.late_fee

    @api.onchange("product_id")
    def _onchange_product_id(self):
        """
        function to change value of minimum day and maximum day
        when we change product_id #T00427
        """
        if self.product_id:
            self.min_day = int(
                self.env["ir.config_parameter"].get_param("book_shelf.min_day")
            )
            self.max_day = int(
                self.env["ir.config_parameter"].get_param("book_shelf.max_day")
            )
