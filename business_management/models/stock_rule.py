from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"  # T00399 inherit object

    def _prepare_purchase_order(self, company_id, origins, values):
        """
        Method to pass value sale to purchase  #T00399
        """
        purchase_value = super()._prepare_purchase_order(
            company_id=company_id, origins=origins, values=values
        )
        purchase_value["about_purchase"] = values[0].get("sale").about_purchase
        return purchase_value

    def _prepare_mo_vals(
        self,
        product_id,
        product_qty,
        product_uom,
        location_id,
        name,
        origin,
        company_id,
        values,
        bom,
    ):
        """
        Method to pass value sale to Manufacturing #T00406
        """
        manufacturing_value = super(StockRule, self)._prepare_mo_vals(
            product_id=product_id,
            product_qty=product_qty,
            product_uom=product_uom,
            location_id=location_id,
            name=name,
            origin=origin,
            company_id=company_id,
            values=values,
            bom=bom,
        )
        manufacturing_value["about_manufacturing"] = values.get("about_manufacturing")
        return manufacturing_value
