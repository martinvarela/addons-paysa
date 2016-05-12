# -*- coding: utf-8 -*-
##############################################################################

##############################################################################

{
    'name': 'Cuotas',
    'version': '1.0',
    'author': 'MVarela',
    'category': 'Deportes',
    'sequence': 10,
    'website': '',
    'summary': 'Cuotas y pagos de Jugadores',
    'description': """
    Cuotas y pagos de Jugadores
    """,
    'depends': ['jugador'],
    'data': [
        'views/cuotas_view.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}