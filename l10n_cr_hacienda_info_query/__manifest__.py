# -*- coding: utf-8 -*-
{
    "name": "Consultar Información de Clientes en Hacienda Costa Rica",
    'version': '17.0.0.0.1',
    'author': 'OdooCR, Singulary, José Artavia, Fabian Artavía',
    'website': "https://github.com/OdooFeCR/FE-CR",
    'license': 'AGPL-3',
    'category': 'Hidden',
    "summary": """Consultar Nombre de Clientes en Hacienda Costa Rica""",
    "description": """Actualización automática de nombre de clientes a partir del API de Hacienda""",
    "depends": [
        'base',
        'contacts',
        'base_setup',
        'l10n_cr_country_codes'
    ],
    "data": [
        'views/res_config_settings_views.xml',
        'data/res_config_settings.xml'
    ],
    "installable": True
}
