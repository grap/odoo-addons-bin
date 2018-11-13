# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models

from .decorator import log_duration


#class StockPicking(models.Model):
#    _inherit = 'stock.picking'

#    @log_duration(pdb_limit=5.0)
#    @api.multi
#    def read(self, fields=None, load='_classic_read'):
#        return super(StockPicking, self).read(fields=fields, load=load)


#class StockMove(models.Model):
#    _inherit = 'stock.move'

#    @log_duration(pdb_limit=5.0)
#    @api.multi
#    def read(self, fields=None, load='_classic_read'):
#        return super(StockMove, self).read(fields=fields, load=load)


#class AccountInvoice(models.Model):
#    _inherit = 'account.invoice'

#    @log_duration(pdb_limit=3.0)
#    @api.multi
#    def read(self, fields=None, load='_classic_read'):
#        return super(AccountInvoice, self).read(fields=fields, load=load)


#class AccountInvoiceLine(models.Model):
#    _inherit = 'account.invoice.line'

#    @log_duration(pdb_limit=1.0)
#    @api.multi
#    def read(self, fields=None, load='_classic_read'):
#        return super(AccountInvoiceLine, self).read(fields=fields, load=load)




#class PurchaseOrder(models.Model):
#    _inherit = 'purchase.order'

#    @log_duration(pdb_limit=3.0)
#    @api.multi
#    def read(self, fields=None, load='_classic_read'):
#        return super(PurchaseOrder, self).read(fields=fields, load=load)


#class PurchaseOrderLine(models.Model):
#    _inherit = 'purchase.order.line'

#    @log_duration(pdb_limit=1.0)
#    @api.multi
#    def read(self, fields=None, load='_classic_read'):
#        return super(PurchaseOrderLine, self).read(fields=fields, load=load)
