
# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################


from openerp.osv.orm import Model
from openerp.osv import fields


class res_partner(Model):
    _inherit='res.partner'


    def _get_grap_value_reference(self, cr, uid, ids, name, arg, context=None): 
        res = {}
        if context is None:
            context = {}
        for aId in ids: 
            res[aId] = "res.partner," + str(aId)
        return res
        
        

    _columns = {
        'grap_value_reference': fields.function(_get_grap_value_reference, type="char"),
    }
