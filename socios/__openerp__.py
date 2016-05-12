# -*- coding: utf-8 -*-
##############################################################################

##############################################################################

{
    'name': 'Socios',
    'version': '1.0',
    'author': 'MVarela',
    'category': 'Deportes',
    'sequence': 10,
    'website': '',
    'summary': 'Socios colaboradores',
    'description': """
    Socios colaboradores
    """,
    'depends': ['jugador'],
    'data': [
        'views/socios_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}