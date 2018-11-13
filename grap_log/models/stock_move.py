# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models

from .decorator import log_duration



class StockMove(models.Model):
    _inherit = 'stock.move'

    @log_duration(pdb_limit=1.0)
    @api.multi
    def read(self, fields=None, load='_classic_read'):
        return super(StockMove, self).read(fields=fields, load=load)

#    @log_duration('coincoin')
#    @api.multi
#    def read(self, fields=None, load='_classic_read'):
#        return super(StockMove, self).read(fields=fields, load=load)
