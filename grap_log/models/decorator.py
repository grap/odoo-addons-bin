# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import pdb
import functools
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def log_duration(
        info_limit=0.0, warning_limit=0.1, error_limit=1.0, pdb_limit=False):

    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            begin_date = datetime.now()
            response = func(self, *args, **kwargs)
            end_date = datetime.now()
            delta = (end_date - begin_date).total_seconds()
            extra_text = ''
            try:
                extra_text += " for %d items" % (len(self.ids))
            except:
                pass
            model_name = self._name.ljust(25)
            func_name = func.func_name.ljust(10)

            message = "[%f] %s %s %s" % (
                delta, model_name, func_name, extra_text)
            if delta > error_limit:
                logger.error('  ' + message)
            elif delta > warning_limit:
                logger.warn(message)
            elif delta > info_limit:
                logger.info('   ' + message)
            else:
                logger.debug('  ' + message)
            if pdb_limit and delta > pdb_limit:
                pdb.set_trace()
            return response
        return wrapper
    return decorator
