from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"  # T00337 inherit object

    def _prepare_invoice_values(self, order, name, amount, so_line):
        """
        Method to pass value sale to invoice  #T00337
        """
        invoice_value = super(SaleAdvancePaymentInv, self)._prepare_invoice_values(
            order, name, amount, so_line
        )
        invoice_value.update({"about_invoice": order.about_invoice})
        return invoice_value
