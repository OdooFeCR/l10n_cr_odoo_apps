# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Importador de Facturas de Proveedores Costa Rica',
    'version': '17.0.0.0.0',
    'category': 'Vendor Bills',
    'author': 'Singulary',
    'license': 'AGPL-3',
    'website': '',
    'summary': 'Import Vendor Bills from incoming mail server',

    'description': """
        
    """,

    # any module necessary for this one to work correctly
    'depends': ['cr_electronic_invoice', 'mail'],

    # always loaded
    'data': [

        'views/res_company_views.xml',
        'views/account_move.xml'
        # 'wizard/cr_multiple_invoice_validation_wz_view.xml',
    ]
    ,
}
