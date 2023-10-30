from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"  # T00411 inherit object

    def _timesheet_create_project_prepare_values(self):
        """
        method to pass value sale order to project  #T00411
        """
        project_value = super(
            SaleOrderLine, self
        )._timesheet_create_project_prepare_values()
        project_value["about_project"] = self.order_id.about_project
        return project_value

    def _timesheet_create_task_prepare_values(self, project):
        """
        method to pass value sale order to task  #T00411
        """
        task_value = super(SaleOrderLine, self)._timesheet_create_task_prepare_values(
            project
        )
        task_value["about_task"] = self.order_id.about_task
        return task_value
