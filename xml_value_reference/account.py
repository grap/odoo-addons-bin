
# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################


from openerp.osv.orm import Model
from openerp.osv import fields


class account_account(Model):
    _inherit='account.account'


    def _get_grap_value_reference(self, cr, uid, ids, name, arg, context=None): 
#        import pdb;pdb.set_trace()
        res = {}
        if context is None:
            context = {}
        for aId in ids: 
            res[aId] = "account.account," + str(aId)
        return res
        
        

    _columns = {
        'grap_value_reference': fields.function(_get_grap_value_reference, type="char"),
    }
