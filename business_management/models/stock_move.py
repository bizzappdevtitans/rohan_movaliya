from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"  # T00391 inherit object

    def _get_new_picking_values(self):
        """
        Method to pass value sale to delivery #T00391
        """
        delivery_value = super(StockMove, self)._get_new_picking_values()
        delivery_value["about_delivery"] = self.group_id.sale_id.about_delivery
        return delivery_value

    def _prepare_procurement_values(self):
        """
        Method to access value of sale #T00399 and #T00406
        """
        values = super(StockMove, self)._prepare_procurement_values()
        # T00399 add value for dictionary for Purchase Order(PO)
        values["sale"] = self.group_id.sale_id
        # T00406 add value in dictionary for Manufacturing Order(MO)
        values["about_manufacturing"] = self.group_id.sale_id.about_manufacturing
        return values
