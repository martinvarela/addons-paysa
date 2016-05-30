# -*- coding: utf-8 -*-
import openerp
from openerp import api, fields, models, tools

class Socios(models.Model):
    _name = 'socios'
    _description = 'Socios'
    #_inherit = ['mail.thread']

    @api.depends('nro_socio', 'nombre')
    def _compute_name(self):
        for record in self:
            record.name = (record.nro_socio or '') + ' - ' + (record.nombre or '')

    name = fields.Char(string="Nro - Nombre", compute='_compute_name', store=True)
    nro_socio = fields.Char(string=u"Número", required=True)
    nombre = fields.Char(string="Nombre")
    direccion = fields.Char(string=u"Dirección")
    cedula = fields.Char(string=u"Cédula")
    celular = fields.Char(string="Celular")
    mail = fields.Char(string="Mail")
    jugador_id = fields.Many2one('jugador', string="Jugador")
    state = fields.Selection(string="Estado", selection=[('s', 'Sin asignar'), ('e', 'Entregado a jugador'), ('v', 'Vendido'), ('p', 'Pago'), ('a', 'Anulado'),], default="s")



class Jugador(models.Model):
    _inherit = 'jugador'

    socios_ids = fields.One2many('socios', 'jugador_id', string="Socios")

