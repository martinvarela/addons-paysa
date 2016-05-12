# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from openerp import api, fields, models, tools

import logging
from datetime import *

_logger = logging.getLogger(__name__)

class Posiciones(models.Model):
    _name = 'penca.posiciones'
    _description = "Posiciones"
    _order = "puntos desc"

    def actualizar_puntajes(self):
        #borro la tabla de posiciones para luego volver a generarla
        self.unlink()
        penca_obj = self.env['penca.penca']
        #inserto los nuevos valores en la tabla de posiciones
        for penca in penca_obj.search([]):
            self.create({'name': penca.name, 'puntos': penca.puntos_total, 'goleador_id': penca.goleador_id.id, 'campeon_id': penca.campeon_id.id})
        return True

    name = fields.Char(string="Nombre", size=80, required=True)
    puntos = fields.Integer(string="Puntos")
    goleador_id = fields.Many2one(comodel_name="penca.goleador", string="Goleador")
    campeon_id = fields.Many2one(comodel_name="penca.equipo", string=u"Campeón")


class Reglas(models.Model):
    _name = 'penca.reglas'
    _description = "Reglamento"

    @api.multi
    def act_puntajes(self):
        posiciones_obj = self.env['penca.posiciones']
        posiciones = posiciones_obj.search([])
        return posiciones.actualizar_puntajes()


class Equipo(models.Model):
    _name = 'penca.equipo'
    _description = "Equipo"

    name = fields.Char(string="Equipo", size=40, required=True)
    escudo = fields.Binary(string="Escudo")


class Partido(models.Model):
    _name = 'penca.partido'
    _description = "Partido"
    _order = 'fecha'

    @api.depends('equipo1_id.name','equipo2_id.name')
    def _concatenar(self):
        for rec in self:
            if not rec.equipo1_id.name or not rec.equipo2_id.name:
                rec.name = ' vs '
            else:
                rec.name = rec.equipo1_id.name  + ' vs ' + rec.equipo2_id.name

    def obtener_puntos(self, resultado, partido):
        #resultado exacto
        if resultado.goles1 == partido.goles_eq1 and resultado.goles2 == partido.goles_eq2 :
            return 6
        #empate
        elif resultado.goles1 == resultado.goles2 and partido.goles_eq1 == partido.goles_eq2 :
            return 4
        #resutlado + diferencia de goles
        elif (resultado.goles1 - resultado.goles2) == (partido.goles_eq1 - partido.goles_eq2) :
            return 4
        elif resultado.goles1 < resultado.goles2 and partido.goles_eq1 < partido.goles_eq2 :
            if (resultado.goles1 == partido.goles_eq1) or (resultado.goles2 == partido.goles_eq2):
                #resultado + goles 1 equipo
                return 4
            else:
                #resultado
                return 3
        elif resultado.goles1 > resultado.goles2 and partido.goles_eq1 > partido.goles_eq2 :
            if (resultado.goles1 == partido.goles_eq1) or (resultado.goles2 == partido.goles_eq2):
                #resultado + goles 1 equipo
                return 4
            else:
                #resultado
                return 3
        elif (resultado.goles1 == partido.goles_eq1) or (resultado.goles2 == partido.goles_eq2):
            #goles 1 equipo
            return 1
        else:
            #nada
            return 0

    @api.multi
    def write(self, vals):
        super(Partido, self).write(vals)
        resultados_obj = self.env['penca.resultado']

        #para cada partido finalizado 
        for partido in self:
            if partido.finalizado == True:
                #busco los pronosticos de ese partido y actualizo los valores
                for resultado in resultados_obj.search([('partido_id','=',partido.id)]):
                    puntos_obtenidos = self.obtener_puntos(resultado, partido)
                    resultado.write({'puntos': puntos_obtenidos})
            elif 'finalizado' in vals and vals['finalizado'] == False:
                resultado_ids = resultados_obj.search([('partido_id','=',partido.id),('puntos','>',0)])
                resultado_ids.write({'puntos': 0})
        return True


    name = fields.Char(string="Partido", compute="_concatenar", store=True)
    fecha = fields.Datetime(string="Fecha", required=True)
    equipo1_id = fields.Many2one(comodel_name="penca.equipo", string="Equipo 1", required=True)
    esc1_related = fields.Binary(string="Escudo1", related="equipo1_id.escudo")
    goles_eq1 = fields.Integer(string="Goles1", size=1)
    equipo2_id = fields.Many2one(comodel_name="penca.equipo", string="Equipo 2", required=True)
    esc2_related = fields.Binary(string="Escudo2", related="equipo2_id.escudo")
    goles_eq2 = fields.Integer(string="Goles2", size=1)
    finalizado = fields.Boolean(string="Finalizado", default=False)

class Resultado(models.Model):
    _name = 'penca.resultado'
    _description = "Resultados"
    _order = 'fecha_related'

    @api.depends('fecha_related')
    def _editable(self):
        for rec in self:
            if rec.fecha_related:
                fecha_partido = datetime.strptime(rec.fecha_related, "%Y-%m-%d %H:%M:%S")
                limite_ingreso = fecha_partido - timedelta(hours=12)
                fecha_actual = datetime.now()
                es_editable = fecha_actual < limite_ingreso
            else:
                es_editable = False
            rec.editable = es_editable

    penca_id = fields.Many2one(comodel_name="penca.penca", string="Penca", ondelete="cascade")
    partido_id = fields.Many2one(comodel_name="penca.partido", string="Partido")
    fecha_related = fields.Datetime(string="Fecha", related="partido_id.fecha", store=True)
    esc1_rel = fields.Binary(string="Escudo1", related="partido_id.equipo1_id.escudo")
    goles1 = fields.Integer(string="Gol1", size=1)
    esc2_rel = fields.Binary(string="Escudo2", related="partido_id.equipo2_id.escudo")
    goles2 = fields.Integer(string="Gol2", size=1)
    puntos = fields.Integer(string="Puntaje Partido", size=2)
    editable = fields.Boolean(string="Editable", compute="_editable")


class Penca(models.Model):
    _name = 'penca.penca'
    _description = "Pencas"

    @api.depends('user_id.name')
    def _obtener_nombre(self):
        for record in self:
            record.name =  record.user_id.name

    @api.depends('resultado_ids.puntos', 'pts_campeon', 'pts_goleador')
    def _calc_ptje(self):
        for record in self:
            ptos = 0
            for resultado in record.resultado_ids:
                ptos += resultado.puntos
            #Sumar goleador y campeon
            ptos += record.pts_campeon + record.pts_goleador
            record.puntos_total = ptos

    #TODO: pasar esto a nivel de configuracion y no un campo funcional
    def _camp_gol_edit(self):
        for record in self:
            fecha_limite = datetime.strptime("2016-06-03 12:00", "%Y-%m-%d %H:%M") #TODO cambiar fecha
            fecha_actual = datetime.now()
            es_editable = fecha_actual < fecha_limite
            record.camp_gol_edit = es_editable

    name = fields.Char(string="Nombre", compute="_obtener_nombre", store="True")
    puntos_total = fields.Integer(string="Puntaje", compute="_calc_ptje")
    pts_campeon = fields.Integer(string="Puntos Campeon")
    pts_goleador = fields.Integer(string="Puntos Goleador")
    goleador_id = fields.Many2one(comodel_name="penca.goleador", string="Goleador")
    campeon_id = fields.Many2one(comodel_name="penca.equipo", string=u"Campeón")
    user_id = fields.Many2one(comodel_name="res.users", string="Usuario")
    resultado_ids = fields.One2many(comodel_name="penca.resultado", inverse_name="penca_id", string="Resultados")
    camp_gol_edit = fields.Boolean(string="Editar camp y gol", compute="_camp_gol_edit")


class CampeonGoleador(models.Model):
    _name = 'penca.campeon_goleador'
    _description = "Campeon y Goleador"
    #_rec_name = 'campeon_id'

    campeon_id = fields.Many2one(comodel_name="penca.equipo", string=u"Campeón")
    goleador_ids = fields.Many2many(comodel_name="penca.goleador", relation="penca_goleador_rel", column1="campeon_goleador_id", column2="goleador_id", string="Goleadores")
    fin = fields.Boolean(string="Finalizo")

    @api.multi
    def write(self, vals):
        super(CampeonGoleador, self).write(vals)
        penca_obj = self.env['penca.penca']

        #obtengo el goleador y el campeon
        for camp_gol in self:
            if camp_gol.fin == True:
                #actualizo todas las pencas
                for penca in penca_obj.search([]):
                    p_camp = 0
                    p_gol = 0                     
                    if camp_gol.campeon_id.id == penca.campeon_id.id:
                        p_camp = 20
                    for goleador in camp_gol.goleador_ids:
                        if goleador.id == penca.goleador_id.id:
                            p_gol = 15
                    if p_camp > 0 or p_gol > 0:
                        penca.write({'pts_campeon': p_camp, 'pts_goleador': p_gol})
            elif 'fin' in vals and vals['fin'] == False:
                penca_ids = penca_obj.search([])
                penca_ids.write({'pts_campeon': 0, 'pts_goleador': 0})
        return True

class Usuario(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, data):
        user_id = super(Usuario, self).create(data)
        #creo la penca asignada al nuevo usuario
        penca_obj = self.env['penca.penca']
        penca_id = penca_obj.create({'user_id': user_id.id})
        #obtengo el modelo resultado para crear nuevos asociados al usuario
        resultado_obj = self.env['penca.resultado']
        #obtengo todos los partidos y para cada uno creo un resultado asociado a la penca
        partido_obj = self.env['penca.partido']
        partido_ids = partido_obj.search([])
        for partido_id in partido_ids:
            resultado_obj.create({'partido_id': partido_id.id, 'penca_id': penca_id.id})
        return user_id

    #_columns = {
    #    'vendedor': fields.char('Vendedor', size=40),
    #}


class Goleador(models.Model):
    _name = 'penca.goleador'
    _description = "Goleador"
    _order = 'goles desc'

    name = fields.Char(string="Nombre", required=True, size=50 )
    foto = fields.Binary(string="Foto")
    goles = fields.Integer(string="Goles")
    equipo_id = fields.Many2one(comodel_name="penca.equipo", string="Equipo")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
