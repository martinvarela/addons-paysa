# -*- coding: utf-8 -*-

from openerp import http
from openerp.http import request
import logging
_logger = logging.getLogger(__name__)

class jugador(http.Controller):

    @http.route(['/page/plantel_mayores'], type='http', auth="public", website=True)
    def mayores(self, **post):
        jugador_obj = request.registry['jugador']
        domain = [('plantel','=','m')]
        if not jugador_obj.check_access_rights(request.cr, request.uid, 'write', raise_exception=False):
            domain.append(('website_published', '=', True))
        jugador_ids = jugador_obj.search(request.cr, request.uid, domain, context=request.context)
        arqueros = []
        defensas = []
        mediocampistas = []
        delanteros = []
        for j in jugador_obj.browse(request.cr, request.uid, jugador_ids, request.context):
            if j.posicion == 'ARQ':
                arqueros.append(j)
            elif j.posicion == 'DEF':
                defensas.append(j)
            elif j.posicion == 'MED':
                mediocampistas.append(j)
            elif j.posicion == 'DEL':
                delanteros.append(j)
            else:
                _logger.info("No tiene posicion")

        cuerpo_tecnico_obj = request.registry['cuerpo_tecnico']
        domain_dts = [('plantel','in',['m','myp'])]
        if not cuerpo_tecnico_obj.check_access_rights(request.cr, request.uid, 'write', raise_exception=False):
            domain_dts.append(('website_published', '=', True))
        cuerpo_tecnico_ids = cuerpo_tecnico_obj.search(request.cr, request.uid, domain_dts, context=request.context)
        tecnicos = cuerpo_tecnico_obj.browse(request.cr, request.uid, cuerpo_tecnico_ids, request.context)

        values = {
            'arqueros_ids': arqueros,
            'defensas_ids': defensas,
            'mediocampistas_ids': mediocampistas,
            'delanteros_ids': delanteros,
            'tecnicos_ids': tecnicos,
        }
        _logger.info("Los valores que manda son: %s", values)
        return request.website.render("jugador.plantel_mayores", values)

    @http.route(['/page/plantel_presenior'], type='http', auth="public", website=True)
    def presenior(self, **post):
        _logger.info("Entro ACA")
        jugador_obj = request.registry['jugador']
        domain = [('plantel','=','p')]
        if not jugador_obj.check_access_rights(request.cr, request.uid, 'write', raise_exception=False):
            domain.append(('website_published', '=', True))
        jugador_ids = jugador_obj.search(request.cr, request.uid, domain, context=request.context)
        arqueros = []
        defensas = []
        mediocampistas = []
        delanteros = []
        for j in jugador_obj.browse(request.cr, request.uid, jugador_ids, request.context):
            if j.posicion == 'ARQ':
                arqueros.append(j)
            elif j.posicion == 'DEF':
                defensas.append(j)
            elif j.posicion == 'MED':
                mediocampistas.append(j)
            elif j.posicion == 'DEL':
                delanteros.append(j)
            else:
                _logger.info("No tiene posicion")

        cuerpo_tecnico_obj = request.registry['cuerpo_tecnico']
        domain_dts = [('plantel','in',['p','myp'])]
        if not cuerpo_tecnico_obj.check_access_rights(request.cr, request.uid, 'write', raise_exception=False):
            domain_dts.append(('website_published', '=', True))
        cuerpo_tecnico_ids = cuerpo_tecnico_obj.search(request.cr, request.uid, domain_dts, context=request.context)
        tecnicos = cuerpo_tecnico_obj.browse(request.cr, request.uid, cuerpo_tecnico_ids, request.context)

        values = {
            'arqueros_ids': arqueros,
            'defensas_ids': defensas,
            'mediocampistas_ids': mediocampistas,
            'delanteros_ids': delanteros,
            'tecnicos_ids': tecnicos,
        }
        _logger.info("Los valores que manda son: %s", values)
        return request.website.render("jugador.plantel_presenior", values)
