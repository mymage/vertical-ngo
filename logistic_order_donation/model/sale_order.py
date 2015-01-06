# -*- coding: utf-8 -*-
#
#
#    Copyright 2014 Camptocamp SA
#    Author: Yannick Vaucher
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
from openerp import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.one
    @api.depends('order_type')
    def _get_line_route_id(self):
        """Compute default order line route id"""
        route_id = False
        if self.order_type == 'donation':
            ref = 'logistic_order_donation.route_donation'
            route_id = self.env['ir.model.data'].xmlid_to_res_id(ref)
        self.line_route_id = route_id

    line_route_id = fields.Many2one(
        compute="_get_line_route_id",
        comodel_name='stock.location.route')

    @api.model
    def get_order_type_selection(self):
        selection = super(SaleOrder, self).get_order_type_selection()
        selection.append(('donation', 'In-Kind Donation'))
        return selection
