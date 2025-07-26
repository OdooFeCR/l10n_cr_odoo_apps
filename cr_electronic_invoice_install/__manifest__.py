{
    'name': 'Instalador de FE Costa Rica',
    'version': '17.0.0.0.0',
    'author': 'Singulary',
    'license': 'AGPL-3',
    'website': 'https://singulary.online',
    'category': 'Accounting/Accounting',
    'description':
        '''
        Facturación electronica Costa Rica.
        ''',
    'depends': [
        'cr_electronic_invoice',
        'cabys',
        'cr_import_vendor_bills',
        'account_financial_report',
        'date_range',
        'report_xlsx'
        ],
    'external_dependencies': {
        "python": [
            'cryptography',
            'xmlsig',
            'OpenSSL',
            'phonenumbers',
            'jsonschema',
        ],
    },
    'installable': True,
    'application': True
}
