# -*- coding: utf-8 -*-
{
    'name': 'Costa Rica Currency Adapter',
    'version': '17.0.0.0.0',
    'author': 'AKUREY S.A., Singulary',
    'license': 'AGPL-3',
    'category': 'Accounting/Accounting',
    'website': "https://github.com/OdooFeCR/FE-CR",
    'depends': [
        'base',
        'account'
    ],
    'data': [
        'data/currency_data.xml',
        'views/res_currency_view.xml',
        'views/res_currency_rate_view.xml',
        'views/res_config_settings_views.xml',
    ],
    'external_dependencies': {
        'python': [
            'zeep'
        ]
    },
    'installable': True,
    'auto_install': False,
}
