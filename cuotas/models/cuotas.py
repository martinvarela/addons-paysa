# -*- coding: utf-8 -*-
import openerp
from openerp import api, fields, models, tools

class Cuotas(models.Model):
    _name = 'cuotas'
    _description = 'Cuotas'
    #_inherit = ['mail.thread']

    name = fields.Char(string=u"Descripción" )
    fecha_pago = fields.Date(string=u"Fecha pago", required=True, default=fields.date.today())
    monto = fields.Integer(string="Monto", required=True )
    jugador_id = fields.Many2one('jugador', string="Jugador", required=True )
    plantel = fields.Selection(related='jugador_id.plantel', store=True)

class OtrosPagos(models.Model):
    _name = 'otros_pagos'
    _description = 'Otros pagos'
    #_inherit = ['mail.thread']
    name = fields.Selection(string="Concepto", selection=[('penca', 'Penca'), ('socios', 'Socios'), ('deuda', u'Deuda año anterior'), ('otro', 'Otro') ], required=True )
    descripcion = fields.Char(string="Descripción" )
    fecha_pago = fields.Date(string=u"Fecha pago", default=fields.date.today())
    monto = fields.Integer(string="Monto", required=True )
    jugador_id = fields.Many2one('jugador', string="Jugador", required=True )
    plantel = fields.Selection(related='jugador_id.plantel', store=True)


class Jugador(models.Model):
    _inherit = 'jugador'

    cuotas_ids = fields.One2many('cuotas', 'jugador_id', string="Cuotas")
    otros_pagos_ids = fields.One2many('otros_pagos', 'jugador_id', string="Otros pagos")
    paga_cuota = fields.Selection(string="Paga cuota para", selection=[('m', 'Mayor'), ('p', 'Pre Senior')])

class ContabilidadMayores(models.Model):
    _name = "contabilidad_mayores"
    _description = "Contabilidad Mayores"

    name = fields.Char(string="Nombre", required=True)
    lineas_ids = fields.One2many("contabilidad_mayores_lineas", "contabilidad_mayores_id", string="Ingresos - Egresos")
    total_cuotas = fields.Integer(compute='_compute_total_cuotas')
    total_otros_pagos = fields.Integer(compute='_compute_total_otros')
    saldo = fields.Integer(compute='_compute_saldo')

    @api.one
    def _compute_total_cuotas(self):
        cuotas_obj = self.env['cuotas']
        ids_cuotas = cuotas_obj.search([('plantel','=','m')])
        total = 0
        for cuota in ids_cuotas:
            total+= cuota.monto
        self.total_cuotas= total

    @api.one
    def _compute_total_otros(self):
        otros_pagos_obj = self.env['otros_pagos']
        ids_otros_pagos = otros_pagos_obj.search([('plantel','=','m')])
        total = 0
        for otro_pago in ids_otros_pagos:
            total+= otro_pago.monto
        self.total_otros_pagos= total

    @api.one
    @api.depends('lineas_ids.monto', 'total_cuotas', 'total_otros_pagos')
    def _compute_saldo(self):
        self.saldo = sum(linea.monto for linea in self.lineas_ids) + self.total_cuotas + self.total_otros_pagos

class ContabilidadMayoresLineas(models.Model):
    _name = 'contabilidad_mayores_lineas'
    _description = 'Lineas Contabilidad Mayores'

    name = fields.Char(string="Concepto", required=True)
    monto = fields.Integer(string="Importe", required=True)
    fecha = fields.Date(string="Fecha", required=True, default=fields.date.today())
    contabilidad_mayores_id = fields.Many2one("contabilidad_mayores", string="Contabilidad Mayores", required=True)

class ContabilidadPresenior(models.Model):
    _name = "contabilidad_presenior"
    _description = "Contabilidad Pre Senior"

    name = fields.Char(string="Nombre", required=True)
    lineas_ids = fields.One2many("contabilidad_presenior_lineas", "contabilidad_presenior_id", string="Ingresos - Egresos")
    total_cuotas = fields.Integer(compute='_compute_total_cuotas')
    total_otros_pagos = fields.Integer(compute='_compute_total_otros')
    saldo = fields.Integer(compute='_compute_saldo')

    @api.one
    def _compute_total_cuotas(self):
        cuotas_obj = self.env['cuotas']
        ids_cuotas = cuotas_obj.search([('plantel','=','p')])
        total = 0
        for cuota in ids_cuotas:
            total+= cuota.monto
        self.total_cuotas= total

    @api.one
    def _compute_total_otros(self):
        otros_pagos_obj = self.env['otros_pagos']
        ids_otros_pagos = otros_pagos_obj.search([('plantel','=','p')])
        total = 0
        for otro_pago in ids_otros_pagos:
            total+= otro_pago.monto
        self.total_otros_pagos= total

    @api.one
    @api.depends('lineas_ids.monto', 'total_cuotas', 'total_otros_pagos')
    def _compute_saldo(self):
        self.saldo = sum(linea.monto for linea in self.lineas_ids) + self.total_cuotas + self.total_otros_pagos

class ContabilidadPreseniorLineas(models.Model):
    _name = 'contabilidad_presenior_lineas'
    _description = 'Lineas Contabilidad Pre Senior'

    name = fields.Char(string="Concepto", required=True)
    monto = fields.Integer(string="Importe", required=True)
    fecha = fields.Date(string="Fecha", required=True, default=fields.date.today())
    contabilidad_presenior_id = fields.Many2one("contabilidad_presenior", string="Contabilidad Pre Senior", required=True)