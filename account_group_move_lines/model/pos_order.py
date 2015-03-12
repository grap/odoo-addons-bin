# -*- encoding: utf-8 -*-
##############################################################################
#
#    Account - Group Move Line Module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
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
##############################################################################

from openerp.tools.translate import _
from openerp.osv.orm import Model


class pos_order(Model):
    _inherit = 'pos.order'

    def _get_key(self, cr, uid, data_type, values, context=None):
        key = False
        if data_type == 'product':
            key = (
                'product', values['tax_code_id'], values['account_id'],
                values['debit'] > 0)
            values.update({'name': _('Various Products')})
        elif data_type == 'tax':
            key = ('tax', values['tax_code_id'], values['debit'] > 0)
        elif data_type == 'counter_part':
            key = ('counter_part', values['account_id'], values['debit'] > 0)
        return key
