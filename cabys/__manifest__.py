{
    'name': "Costa Rica -Catálogo de bienes y servicios para uso tributario y Cuentas Nacionales",

    'summary': "Catálogo de bienes y servicios para uso tributario y Cuentas Nacionales",
    'author': 'info@fakturacion.com | Singulary | Fabian Artavia',
    'website': "https://github.com/OdooFeCR/FE-CR",
    'category': 'Account',
    'version': '17.0.1.0.0',
    'license': 'AGPL-3',
    'price': 0,
    'currency': 'USD',
    'depends': [
        'base',
        'account',
        'product',
    ],
    'data': [
        'views/cabys_producto_views.xml',
        'data/pharmaceutical_forms_data.xml',
        'views/pharmaceutical_form_views.xml',
        'views/cabys_views.xml',
        'views/product_product_views.xml',
        'views/product_template_views.xml',
        'views/product_category_views.xml',
        'views/res_company_views.xml',
        'wizard/cabys_catalog_import_wizard.xml',
        'security/ir.model.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
            'web.core',
            'web.ListController',
            'cabys.cabys_import_button.js',
      ],
        'web.assets_qweb': [
            'cabys.cabys_templates.xml',
        ]
    },
    'installable': True,
}
