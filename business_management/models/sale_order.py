from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"  # T00377 inherit object

    # T00377 added fields
    about_invoice = fields.Text()

    # T00391 added fields
    about_delivery = fields.Text()

    # T00399 added fields
    about_purchase = fields.Text()

    # T00406 added fields
    about_manufacturing = fields.Text()

    # T00411 added fields
    about_project = fields.Text()
    about_task = fields.Text()

    def _prepare_invoice(self):
        """
        Method to pass value sale to invoice  #T00337
        """
        invoice_value = super(SaleOrder, self)._prepare_invoice()
        invoice_value["about_invoice"] = self.about_invoice
        return invoice_value
