# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
#OK: Datos de equipos y partidos por XML
#OK: Que no sea necesario el modelo de posiciones, que se vea lo de la penca OK
#OK: Hacer modelo a partir de vista sql para posiciones en backend
#OK: Reglas de seguridad y listas de control de acceso, roles: Usuario Penca, Admin Penca
#TODO TERMINAR DE MEJORAR: Paginas en la web con las posiciones, información y reglas
#TEST: mejorar envio de mails: "paysanduuniversitario@gmail.com"/"paysa2016." cambiar traduccion del template de envio de mail, cambiar direccion de mail de la compañia y del admin
#OK: mejorar creacion de pencas automatico
#TODO: revisar criterio de puntos, campeon, goleador y partido, darle mas importancia a un 4 a 2 que a un 1 a 0
#TESTEAR: validacion de que no hagan trampa readonly al guardar
#TODO: Ocultar menus mensajeria e informes
#TESTEAR: (Se resuelve con form vacio) desde la tree de los resultados de la penca se puede abrir la form y editar los campos y deja editar los puntos y goles
{
    'name': 'Penca Copa America Centenario - Pay 2016',
    'version': '1.0',
    'author': 'mvarela',
    'website': 'www.paysanduniversitario.tk',
    'category': 'General',
    'images': [],
    'depends': ['website','web_tree_image', 'web_m2x_options'],
    'description': """
Penca de la Copa America Centenario 2016 - Paysandu Universitario """,
    'demo': [],
    'test': [],
    'data': [
        'security/penca_security.xml',
        'views/penca_view.xml',
        'views/config_penca_view.xml',
        'templates/penca_template.xml',
        'security/ir.model.access.csv',
        'views/penca_data.xml',
    ],
    'installable': True,
    'auto_install': False,
}
