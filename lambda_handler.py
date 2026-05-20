import json
import os

CORS_ORIGIN = os.getenv('CORS_ORIGIN', '*')

CORS_HEADERS = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': CORS_ORIGIN,
    'Access-Control-Allow-Headers': 'Content-Type,Authorization',
    'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
}


def resp(status, body):
    return {'statusCode': status, 'headers': CORS_HEADERS, 'body': json.dumps(body, ensure_ascii=False)}


# ── Mock data ──────────────────────────────────────────────────────────────────

CAMPANIAS = [
    {'id_campania': 1, 'nombre': 'Renovación Proactiva', 'estado': 'activa'},
    {'id_campania': 2, 'nombre': 'Captación Nuevos Clientes', 'estado': 'activa'},
]

PUESTOS = [
    {'id_puesto': 1, 'nombre': 'Asesor de Ventas', 'estado': 'activo'},
    {'id_puesto': 2, 'nombre': 'Supervisor de Turno', 'estado': 'activo'},
    {'id_puesto': 3, 'nombre': 'Analista de Calidad', 'estado': 'activo'},
]

REQUERIMIENTOS = [
    {
        'id_requerimiento': 1, 'codigo': 'RQ001',
        'id_campania': 1, 'campania': 'Renovación Proactiva',
        'id_puesto': 1, 'puesto': 'Asesor de Ventas',
        'cantidad': 10, 'estado': 'abierto',
        'fecha_inicio_capacitacion': '2026-05-25',
        'fecha_fin_capacitacion': '2026-05-30',
        'dias_capacitacion': 10,
        'fecha_ingreso': '2026-06-01',
    },
    {
        'id_requerimiento': 2, 'codigo': 'RQ002',
        'id_campania': 2, 'campania': 'Captación Nuevos Clientes',
        'id_puesto': 2, 'puesto': 'Supervisor de Turno',
        'cantidad': 3, 'estado': 'abierto',
        'fecha_inicio_capacitacion': '2026-06-01',
        'fecha_fin_capacitacion': '2026-06-05',
        'dias_capacitacion': 5,
        'fecha_ingreso': '2026-06-10',
    },
]

POSTULACIONES = [
    {
        'id_postulacion': 1, 'id_requerimiento': 1, 'codigo_rq': 'RQ001',
        'dni': '12345678', 'nombre': 'Juan Pérez', 'apellido': 'García',
        'correo': 'juan@example.com', 'telefono': '999111222',
        'estado': 'nueva', 'requisito_revisado': False, 'apto': None,
        'entrevista_aprobada': None, 'contratar': None,
        'fecha_postulacion': '2026-05-15',
    },
    {
        'id_postulacion': 2, 'id_requerimiento': 1, 'codigo_rq': 'RQ001',
        'dni': '87654321', 'nombre': 'María', 'apellido': 'López',
        'correo': 'maria@example.com', 'telefono': '999333444',
        'estado': 'entrevista', 'requisito_revisado': True, 'apto': True,
        'entrevista_aprobada': None, 'contratar': None,
        'fecha_postulacion': '2026-05-16',
    },
]

_next_id = {'rq': 3, 'post': 3}


def lambda_handler(event, context):
    method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    body = {}
    if event.get('body'):
        try:
            body = json.loads(event['body'])
        except Exception:
            pass

    # Strip /v1 prefix
    if path.startswith('/v1'):
        path = path[3:]

    # OPTIONS (CORS preflight)
    if method == 'OPTIONS':
        return resp(200, {})

    # ── Campañas ──────────────────────────────────────────────────────────────
    if method == 'GET' and path == '/campanias/activas':
        return resp(200, {'campanias': CAMPANIAS})

    if method == 'POST' and path == '/campanias':
        nueva = {'id_campania': len(CAMPANIAS) + 1, **body, 'estado': 'activa'}
        CAMPANIAS.append(nueva)
        return resp(201, {'campania': nueva})

    # ── Puestos ───────────────────────────────────────────────────────────────
    if method == 'GET' and path == '/puestos/activos':
        return resp(200, {'puestos': PUESTOS})

    if method == 'POST' and path == '/puestos':
        nuevo = {'id_puesto': len(PUESTOS) + 1, **body, 'estado': 'activo'}
        PUESTOS.append(nuevo)
        return resp(201, {'puesto': nuevo})

    # ── Requerimientos ────────────────────────────────────────────────────────
    if method == 'GET' and path == '/requerimientos':
        return resp(200, {'requerimientos': REQUERIMIENTOS})

    if method == 'POST' and path == '/requerimientos':
        codigo = f"RQ{_next_id['rq']:03d}"
        _next_id['rq'] += 1
        nuevo = {'id_requerimiento': _next_id['rq'], 'codigo': codigo, **body, 'estado': 'abierto'}
        REQUERIMIENTOS.append(nuevo)
        return resp(201, {'requerimiento': nuevo})

    if method == 'GET' and path.startswith('/requerimientos/') and path.count('/') == 2:
        codigo = path.split('/')[-1]
        rq = next((r for r in REQUERIMIENTOS if r['codigo'] == codigo), None)
        if not rq:
            return resp(404, {'error': 'Requerimiento no encontrado'})
        return resp(200, {'requerimiento': rq})

    # ── Postulaciones ─────────────────────────────────────────────────────────
    if method == 'GET' and path.endswith('/postulaciones'):
        # GET /requerimientos/{codigo}/postulaciones
        codigo = path.split('/')[-2] if '/postulaciones' in path else None
        rq = next((r for r in REQUERIMIENTOS if r['codigo'] == codigo), None) if codigo else None
        rq_id = rq['id_requerimiento'] if rq else None
        posts = [p for p in POSTULACIONES if rq_id is None or p['id_requerimiento'] == rq_id]
        return resp(200, {'postulaciones': posts})

    if method == 'POST' and path == '/postulaciones':
        nueva = {
            'id_postulacion': _next_id['post'],
            'id_requerimiento': body.get('requerimiento_id'),
            'estado': 'nueva',
            'requisito_revisado': False, 'apto': None,
            'entrevista_aprobada': None, 'contratar': None,
            'fecha_postulacion': '2026-05-20',
            **body,
        }
        _next_id['post'] += 1
        POSTULACIONES.append(nueva)
        return resp(201, {'postulacion': nueva, 'message': 'Postulación registrada exitosamente'})

    if method == 'PUT' and path.endswith('/estado'):
        parts = path.split('/')
        try:
            post_id = int(parts[-2])
        except (ValueError, IndexError):
            return resp(400, {'error': 'ID inválido'})
        post = next((p for p in POSTULACIONES if p['id_postulacion'] == post_id), None)
        if not post:
            return resp(404, {'error': 'Postulación no encontrada'})
        post.update(body)
        return resp(200, {'postulacion': post})

    return resp(404, {'error': 'Endpoint no encontrado', 'path': path, 'method': method})
