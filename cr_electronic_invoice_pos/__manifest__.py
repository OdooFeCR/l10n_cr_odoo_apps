# -*- coding: utf-8 -*-
{
    'name': 'Facturación electrónica Costa Rica POS',
    'version': '17.0.0.0.0',
    'author': 'Singulary',
    'license': 'AGPL-3',
    'website': 'https://singulary.online',
    'category': 'Account',
    'description':
    '''
    Facturación electronica POS Costa Rica.
    ''',
    'depends': [
        'cr_electronic_invoice',
        'point_of_sale',
        'l10n_cr_hacienda_info_query'
    ],
    'data': [
        'data/res.partner.csv',
        'views/res_config_settings_view.xml',
        'views/pos_payment_method_form.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'cr_electronic_invoice_pos/static/src/js/models.js',
            'cr_electronic_invoice_pos/static/src/js/payment_screen.js',
            'cr_electronic_invoice_pos/static/src/xml/custom_orderReceipt.xml',
        ],
    },
    'installable': True,
}
