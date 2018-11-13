# -*- encoding: utf-8 -*-
##############################################################################
#
#    Product - Improved Search Module for Odoo
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

from openerp.osv.orm import Model
from openerp.osv.expression import get_unaccent_wrapper
from openerp import SUPERUSER_ID
import string


class product_product(Model):
    _inherit = 'product.product'

    # Constant Values
    _MULTI_SEARCH_SEPARATOR = ':'
    _MULTI_SEARCH_REPLACEMENT = ''

    _MULTI_SEARCH_OPERATORS = ['not ilike', 'ilike']
    _MULTI_SEARCH_FIELDS = ['name', 'default_code']

    def name_search(
            self, cr, uid, name, args=None, operator='ilike', context=None,
            limit=100):
        if not args:
            args = []
        if name and operator in ('=', 'ilike', '=ilike', 'like', '=like'):
            unaccent = get_unaccent_wrapper(cr)
            self.check_access_rights(cr, uid, 'read')
            where_query = self._where_calc(cr, uid, args, context=context)
            self._apply_ir_rules(cr, uid, where_query, 'read', context=context)
            from_clause, where_clause, where_clause_params =\
                where_query.get_sql()
            where_str = where_clause\
                and (" WHERE %s AND " % where_clause) or ' WHERE '

            if "product_product__product_tmpl_id" not in from_clause:
                from_clause +=\
                    ',"product_template" as "product_product__product_tmpl_id"'
            if operator in ('ilike', 'like'):
                percent = True
            if operator in ('=ilike', '=like'):
                operator = operator[1:]

            names = name.split(self._MULTI_SEARCH_SEPARATOR)
            pwc = ""
            for n in names:
                search_name = '%%%s%%' % n if percent else n
                pwc += """ AND ({display_name} {operator} {percent})
                """.format(
                    operator=operator, percent=unaccent('%s'),
                    display_name=unaccent(
                        'product_product__product_tmpl_id.name'))
                where_clause_params += [search_name]
            pwc = pwc[5:]

            query = """SELECT product_product.id
                         FROM {from_clause}
                      {where} ({pwc})
                     ORDER BY {display_name}
                    """.format(
                    from_clause=from_clause, where=where_str, pwc=pwc,
                    display_name=unaccent(
                        'product_product__product_tmpl_id.name'))

            if limit:
                query += ' limit %s'
                where_clause_params.append(limit)

            cr.execute(query, where_clause_params)
            ids = map(lambda x: x[0], cr.fetchall())

            if ids:
                return self.name_get(cr, uid, ids, context)
            else:
                return []
        return super(product_product, self).name_search(
            cr, uid, name, args, operator=operator, context=context,
            limit=limit)

    def search(
            self, cr, uid, args, offset=0, limit=None, order=None,
            context=None, count=False):
        copy_args = list(args)
        for arg in copy_args:
            if isinstance(arg, (tuple, list)) and len(arg) == 3:
                name, operator, value = arg
                if name in self._MULTI_SEARCH_FIELDS and\
                        operator in self._MULTI_SEARCH_OPERATORS and\
                        self._MULTI_SEARCH_SEPARATOR in value:
                    criterias = value.split(self._MULTI_SEARCH_SEPARATOR)
                    new_arg_lst = [
                        (name, operator, x) for x in criterias if x != '']
                    args = args[:args.index(arg)] +\
                        ['&'] * (len(new_arg_lst) - 1) + new_arg_lst +\
                        args[args.index(arg)+1:]
        return super(product_product, self).search(
            cr, uid, args, offset=offset, limit=limit, order=order,
            context=context, count=count)

    def _replace_separator(self, cr, uid, ids=None, context=None):
        product_ids = super(product_product, self).search(cr, SUPERUSER_ID, [
            ('name', 'like', '%' + self._MULTI_SEARCH_SEPARATOR + '%')],
            context=context)
        for product in self.browse(
                cr, SUPERUSER_ID, product_ids, context=context):
            new_name = string.replace(
                product.name, self._MULTI_SEARCH_SEPARATOR,
                self._MULTI_SEARCH_REPLACEMENT)
            self.write(
                cr, SUPERUSER_ID, [product.id], {
                    'name': new_name,
                }, context=context)
        return product_ids
