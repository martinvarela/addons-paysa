# -*- coding: utf-8 -*-
##############################################################################

##############################################################################

{
    'name': 'Jugadores',
    'version': '1.0',
    'author': 'MVarela',
    'category': 'Deportes',
    'sequence': 10,
    'website': '',
    'summary': 'Jugadores',
    'description': """
    Modulo de manejo de jugadores
    """,
    'depends': ['base','website','mail'],
    'data': [
        'data/data.xml',
        'views/jugador_view.xml',
        'views/jugador_template.xml',
        'security/jugador_security.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'qweb': [],
}