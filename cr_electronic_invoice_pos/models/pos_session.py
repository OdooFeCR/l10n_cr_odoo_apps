# -*- coding: utf-8 -*-
# Module develop by @jartavia05

from odoo import models, fields, api

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_res_company(self):
        result = super()._loader_params_res_company()
        result['search_params']['fields'].append('invoice_is_electronic')
        return result