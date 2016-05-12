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
#TODO: Datos de equipos, partidos y jugadores por XML
#TODO: Que no sea necesario el modelo de posiciones, que se vea lo de la penca
#TODO: Reglas de seguridad y listas de control de acceso, roles: Usuario Penca, Admin Penca
#TODO: Paginas en la web con las posiciones y información
#TODO: parametrizar fechas limites
#TODO: automatizar puntajes y posiciones
#TODO: mejorar envio de mails y creacion de pencas
#TODO: validacion de que no hagan trampa readonly al guardar
{
    'name': 'Penca Copa America Centenario - Pay 2016',
    'version': '1.0',
    'author': 'mvarela',
    'website': 'www.paysanduniversitario.tk',
    'category': 'General',
    'images': [],
    'depends': ['web_tree_image', 'web_m2x_options'],
    'description': """
Penca de la Copa America Centenario 2016 - Paysandu Universitario """,
    'demo': [],
    'test': [],
    'data': [
        'views/penca_view.xml',
        'views/config_penca_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
