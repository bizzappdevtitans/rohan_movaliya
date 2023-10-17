from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class BookShelf(models.Model):
    _name = "book.shelf"
    _description = "Book Shelf"
    _rec_name = "partner_id"

    # T00427 added fields
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner", required=True
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("process", "Process"),
            ("confirm", "Confirm"),
            ("cancelled", "Cancelled"),
        ],
        string="States",
        default="draft",
        readonly=True,
    )
    shelf_line_ids = fields.One2many(
        comodel_name="book.shelf.line", inverse_name="shelf_id", string="Shelf Lines"
    )
    sale_order_ref = fields.Char(string="Sale Order Reference", readonly=True)
    order_confirm_date = fields.Date(string="Order confirm Date", readonly=True)
    book_shelf_no = fields.Char(
        string="Book Shelf No.",
        required=True,
        readonly=True,
        default=lambda self: _("Book Shelf No"),
    )

    def confirm_shelf(self):
        """
        function to pass value book.shelf to sale.order and book.self.line to
        sale.order.line #T00427
        """

        # T00427 pass value book shelf to sale order
        sale_order = self.env["sale.order"].create(
            {
                "partner_id": self.partner_id.id,
                "date_order": fields.Date.today(),
            }
        )
        # T00427 pass value book shelf line to  sale order line
        for line in self.shelf_line_ids:
            if not line.product_id.is_issued:
                sale_order_line = self.env["sale.order.line"].create(  # noqa: F841
                    {
                        "order_id": sale_order.id,
                        "product_id": line.product_id.id,
                        "product_uom_qty": 1,
                        "price_unit": 0,
                        "tax_id": False,
                    }
                )
                line.product_id.is_issued = True
        self.sale_order_ref = sale_order.name
        self.state = "process"

    def return_book(self):
        """
        function for process return book #T00427
        """
        return_date = date.today()
        # T00427 calculate days difference between issue and return
        days_difference = (return_date - self.order_confirm_date).days
        # T00427  calculate charges for in case miss deadline
        charge = self.shelf_line_ids.late_fee * (
            days_difference - self.shelf_line_ids.max_day
        )

        # T00427 raise error accorgingly days difference
        if days_difference < self.shelf_line_ids.min_day:
            raise ValidationError(_("You cannot return book before mimimum day"))
        elif days_difference > self.shelf_line_ids.max_day:
            raise ValidationError(
                _(f"You Missed Deadline \nYou have to pay charges \nCharges={charge}")
            )
        else:
            raise ValidationError(_("Your Book Return Process is Successfully"))

    def action_view_issued_books(self):
        """
        smart button for partner issued book #T00427
        """
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Issued Books",
            "view_mode": "tree,form",
            "res_model": "book.shelf.line",
            "domain": [("product_id", "=", self.shelf_line_ids.product_id.id)],
            "context": "{'create': False}",
        }

    @api.model
    def create(self, vals):
        """function to generate unique book shelf number
        for each new book shelf #T00427
        """
        vals["book_shelf_no"] = self.env["ir.sequence"].next_by_code("book.shelf")
        return super(BookShelf, self).create(vals)
