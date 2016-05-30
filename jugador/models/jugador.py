# -*- coding: utf-8 -*-
from openerp import api, fields, models, tools

class Jugador(models.Model):
    _name = 'jugador'
    _description = 'Jugador'
    _inherit = ['mail.thread']

    name = fields.Char(string="Nombre", required=True, )
    fecha_nacimiento = fields.Date(string="Fecha de nacimiento")
    telefono = fields.Char(string=u"Teléfono")
    direccion = fields.Char(string=u"Dirección")
    plantel = fields.Selection(string="Plantel", selection=[('m', 'Mayores'), ('p', 'Pre Senior')], required=True )
    vencimiento_carne = fields.Date(string=u"Vencimiento carné jugador")
    vencimiento_ficha_medica = fields.Date(string=u"Vencimiento ficha médica")
    ultimo_examen = fields.Date(string=u"Último examen")
    posicion = fields.Selection(string=u"Posición", selection=[('ARQ', 'Arquero'), ('DEF', 'Defensa'), ('MED', 'Mediocampista'), ('DEL', 'Delantero')])
    website_published = fields.Boolean(string="Publicado en sitio web")
    image_medium = fields.Binary(string="Foto")
    notes = fields.Text(string="Notas")
    cedula = fields.Char(string=u"Nro cédula")
    nro_carne = fields.Char(string=u"Nro carné")

    @api.model
    def create(self, values):
        if values.get('image_medium'):
            mediana = tools.image_resize_image_medium(values.get('image_medium'))
            values.update({'image_medium': mediana})
        return super(Jugador, self).create(values)

    @api.multi
    def write(self, values):
        if values.get('image_medium'):
            mediana = tools.image_resize_image_medium(values.get('image_medium'))
            values.update({'image_medium': mediana})
        return super(Jugador, self).write(values)

class CuerpoTecnico(models.Model):
    _name = 'cuerpo_tecnico'
    _description = u'Cuerpo Técnico'

    name = fields.Char(string="Nombre", required=True, )
    plantel = fields.Selection(string="Plantel", selection=[('m', 'Mayores'), ('p', 'Pre Senior'), ('myp', 'Mayores y Pre Senior')], required=True )
    puesto = fields.Selection(string="Puesto", selection=[('dt', u'Director técnico'), ('pf', u'Preparador físico'), ('ayu', u'Ayudante técnico')])
    website_published = fields.Boolean(string="Publicado en sitio web")
    image_medium = fields.Binary(string="Foto")
    notes = fields.Text(string="Notas")

    @api.model
    def create(self, values):
        if values.get('image_medium'):
            mediana = tools.image_resize_image_medium(values.get('image_medium'))
            values.update({'image_medium': mediana})
        return super(CuerpoTecnico, self).create(values)

    @api.multi
    def write(self, values):
        if values.get('image_medium'):
            mediana = tools.image_resize_image_medium(values.get('image_medium'))
            values.update({'image_medium': mediana})
        return super(CuerpoTecnico, self).write(values)
