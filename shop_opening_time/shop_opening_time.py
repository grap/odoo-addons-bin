# -*- coding: utf-8 -*-

from datetime import date, datetime, time, timedelta
from openerp.osv import fields, osv
from openerp.osv.orm import Model
from openerp.tools.translate import _

_SHOP_OPENING_TIME_STATE = [('futur', 'Futur times'),('current', 'Current times'),('past', 'Past times'),]

class shop_opening_time(Model):
    _name = "shop.opening.time"
    _description = "Opening time of shop"

    _order = "shop_id,start_date"
    
    ### Columns section
    def _get_state(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if context is None:
            context = {}
        for sot in self.browse(cr, uid, ids, context=context):
            if datetime.strptime(sot.start_date, "%Y-%m-%d") > datetime.today(): 
                res[sot.id] = 'futur'
            elif sot.stop_date and datetime.strptime(sot.stop_date, "%Y-%m-%d")+timedelta(days=1) < datetime.today():
                res[sot.id] = 'past'
            else:
                res[sot.id] = 'current'
        return res

    def _get_weekly_opening_hours(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if context is None:
            context = {}
        for sot in self.browse(cr, uid, ids, context=context):
            res[sot.id] = 0
            for sotl in sot.line_ids: 
                res[sot.id] += sotl.opening_hours
        return res
        
    def _get_complete_name(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if context is None:
            context = {}
        for sot in self.browse(cr, uid, ids, context=context):
            res[sot.id] = sot.shop_id.name + ' - ' + sot.name
        return res

    _columns = {
        'shop_id': fields.many2one('sale.shop', 'Sale shop', 
            required=True, ondelete="cascade",),
        'company_id': fields.related('shop_id', 'company_id', type='many2one', 
            relation='res.company', string='Company', store=True,),
        'name': fields.char('Name', size=64, required=True,),
        'complete_name': fields.function(_get_complete_name, type="char", string='Complete name'),
        'line_ids': fields.one2many('shop.opening.time.line', 'shop_opening_time_id', 
            string='List of line of opening time of shop',),
        'start_date': fields.date('Start date', required=True, 
            help='First monday when the opening time is used',),
        'stop_date': fields.date('End date', 
            help='Last sunday when the opening time is used. (Day included)',),
        'state': fields.function(_get_state, type='selection', string='Status', 
            selection=_SHOP_OPENING_TIME_STATE,
            help='Computed field. To change it, change the start or end date fields.',),
        'weekly_opening_hours': fields.function(_get_weekly_opening_hours, 
            type='float', string='Weekly opening hours',),
    }

    ### Constraints section
    def _check_start_date_stop_date_day(self, cr, uid, ids, context=None):
        for sot in self.browse(cr, uid, ids, context=None):
            if datetime.strptime(sot.start_date, "%Y-%m-%d").isoweekday() != 1 or \
                (sot.stop_date and 
                datetime.strptime(sot.stop_date, "%Y-%m-%d").isoweekday() !=7):
                return False
        return True

    def _check_start_date_stop_date_order(self, cr, uid, ids, context=None):
        for sot in self.browse(cr, uid, ids, context=None):
            if sot.stop_date and sot.stop_date < sot.start_date: 
                return False
        return True
        
    def _check_period_superposition(self, cr, uid, ids, context=None):
        for sot in self.browse(cr, uid, ids, context=None):
            if not sot.stop_date:
                domain = ['|', 
                    ('stop_date', '=', False),
                    ('stop_date', '>', sot.start_date),
            ]
                if self.search_count(cr, uid, domain, context=context) > 1:
                    return False
            else:
                domain = ['&', 
                    ('start_date', '<', sot.stop_date), 
                    '|', 
                    ('stop_date', '=', False), 
                    ('stop_date', '>', sot.start_date),
            ]
                if self.search_count(cr, uid, domain, context=context) > 1:
                    return False
        return True

    _constraints = [
            (_check_start_date_stop_date_day, _('Error ! Start day must be a monday and end day a sunday.'), ['start_date','stop_date'],),
            (_check_start_date_stop_date_order, _('Error ! You can not define end date before start date.'), ['start_date','stop_date'],),
            (_check_period_superposition, _('Error ! The opening times period is in conclict with other(s).'), ['start_date','stop_date'],),
        ]

    ### Overloads section
    def copy(self, cr, uid, id, default=None, context=None):
        """
        We assume that duplicate button is used to create a new opening times
        based on the precedent opening times configuration for the next weeks.
        """
        sot = self.browse(cr, uid, [id], context=context)[0]
        if not sot.stop_date:
            raise osv.except_osv(_('Error!'), _('Unable to duplicate shop opening time with unset end date.'))
        d = {
            'start_date': datetime.strptime(sot.stop_date, "%Y-%m-%d")+timedelta(days=1),
            'stop_date': False,
        }
        return super(shop_opening_time, self).copy(cr, uid, id, d, context=context)

    ### Views section
    def onchange_start_date(self, cursor, user, ids, start_date):
        if not start_date:
            return {}
        else:
            dt_start_date = datetime.strptime(start_date, "%Y-%m-%d")
            start_date = dt_start_date + timedelta(days=1 - dt_start_date.isoweekday())
            return {'value': {'start_date': str(start_date)}}

    def onchange_stop_date(self, cursor, user, ids, stop_date):
        if not stop_date:
            return {}
        else:
            dt_stop_date = datetime.strptime(stop_date, "%Y-%m-%d")
            stop_date = dt_stop_date + timedelta(days=7 - dt_stop_date.isoweekday())
            return {'value': {'stop_date': str(stop_date)}}

class shop_opening_time_line(Model):
    _name = "shop.opening.time.line"
    _description = "Line of opening time of shop"
    
    ### Columns section
    def _get_opening_hours(self, cr, uid, ids, name, arg, context=None):
        res = {}
        if context is None:
            context = {}
        for sotl in self.browse(cr, uid, ids, context=context):
            res[sotl.id] = sotl.closing_hour - sotl.opening_hour
        return res

    _columns = {
        'shop_opening_time_id': fields.many2one('shop.opening.time', 
            'Opening time of shop', required=True, ondelete="cascade",),
        'shop_id': fields.related('shop_opening_time_id', 'shop_id', 
            type='many2one', relation='sale.shop', string='Sale shop'),
        'company_id': fields.related('shop_opening_time_id', 'company_id', 
            type='many2one', relation='res.company', string='Company', store=True),
        'day': fields.selection([('1','Monday'),('2','Tuesday'),('3','Wednesday'),('4','Thursday'),('5','Friday'),('6','Saturday'),('7','Sunday')], 'Day of week', required=True,),
        'opening_hour': fields.float('Opening hour', required=True,),
        'closing_hour': fields.float('Closing hour', required=True,),
        'opening_hours': fields.function(_get_opening_hours, type='float', 
            string='Opening hours',),
        'state': fields.related('shop_opening_time_id', 'state', type='selection', 
            selection=_SHOP_OPENING_TIME_STATE,),
    }
    
    ### Constraints section
    def _check_opening_hour_closing_hour_value(self, cr, uid, ids, context=None):
        for sotl in self.browse(cr, uid, ids, context=None):
            if sotl.opening_hour <0 or \
                sotl.opening_hour >= 24 or \
                sotl.closing_hour <0 or \
                sotl.closing_hour > 24 :
                return False
        return True

    def _check_opening_hour_closing_hour_order(self, cr, uid, ids, context=None):
        for sotl in self.browse(cr, uid, ids, context=None):
            if sotl.closing_hour <= sotl.opening_hour: 
                return False
        return True
        
    def _check_hours_superposition(self, cr, uid, ids, context=None):
        for sotl in self.browse(cr, uid, ids, context=None):
            domain = ['&', 
                ('shop_opening_time_id', '=', sotl.shop_opening_time_id.id),
                '&', 
                ('day', '=', sotl.day),
                '&', 
                ('opening_hour', '<', sotl.closing_hour), 
                ('closing_hour', '>', sotl.opening_hour),
            ]
            if self.search_count(cr, uid, domain, context=context) > 1:
                return False
        return True

    _constraints = [
            (_check_opening_hour_closing_hour_value, _('Error ! Opening and closing hours must be ordered and between 0:00 and 24:00.'), ['opening_hour','closing_hour'],),
            (_check_opening_hour_closing_hour_order, _('Error ! You can not define closing hour before opening hour.'), ['opening_hour','closing_hour'],),
            (_check_hours_superposition, _('Error ! The opening hours period is in conclict with other(s).'), ['opening_hour','closing_hour'],),
    ]
