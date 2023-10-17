from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_view_book_shelf(self):
        """
        smart button for sale.order showing book.shelf #T00427
        """
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Book Shelf",
            "view_mode": "tree,form",
            "res_model": "book.shelf",
            "domain": [("partner_id", "=", self.partner_id.id)],
            "context": "{'create': False}",
        }

    def action_confirm(self):
        """
        function when we confirm sale order confirmation date will be set in book
        shelf abd state change process --> confirm #T00427
        """
        values = self.env["book.shelf"].search([("sale_order_ref", "=", self.name)])
        values.state = "confirm"
        values.order_confirm_date = self.date_order
        return super(SaleOrder, self).action_confirm()

    def action_cancel(self):
        """
        function when we cancle sale order and state change
           process --> cancllead #T00427
        """
        values = self.env["book.shelf"].search([("sale_order_ref", "=", self.name)])
        values.state = "cancelled"

        return super(SaleOrder, self).action_cancel()
