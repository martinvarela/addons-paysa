# -*- coding: utf-8 -*-

from openerp import http
from openerp.http import request
import logging
_logger = logging.getLogger(__name__)


class jugador(http.Controller):

    @http.route(['/page/penca_posiciones'], type='http', auth="public", website=True)
    def posiciones(self, **post):
        penca_obj = request.registry['penca.penca']
        goleador_obj = request.registry['penca.goleador']
        #if not penca_obj.check_access_rights(request.cr, request.uid, 'write', raise_exception=False):
        #    domain.append(('website_published', '=', True))
        penca_ids = penca_obj.search(request.cr, request.uid, [], context=request.context)
        pencas = []
        pencas_desord = []
        for p in penca_obj.browse(request.cr, request.uid, penca_ids, request.context):
            pencas_desord.append((p, p.puntos_total))
        pencas_ord =  sorted(pencas_desord, key=lambda l: l[1], reverse=True)

        pencas = [penca[0] for penca in pencas_ord]

        #goleador_ids = goleador_obj.search(request.cr, request.uid, [('goles','>',0)], order="goles desc", limit=10, context=request.context)
        goleador_ids = goleador_obj.search(request.cr, request.uid, [], order="goles desc", limit=10, context=request.context)

        goleadores = []
        for g in goleador_obj.browse(request.cr, request.uid, goleador_ids, request.context):
            goleadores.append(g)

        values = {
            'penca_ids': pencas,
            'goleador_ids': goleadores,
        }
        _logger.info("Los valores que manda son: %s", values)
        return request.website.render("penca.penca_posiciones", values)

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
