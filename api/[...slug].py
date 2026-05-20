from http.server import BaseHTTPRequestHandler
import json
import os
import uuid
from datetime import datetime
import urllib.parse

DB_FILE = '/tmp/candidatos.json'

INITIAL_CANDIDATOS = [
    {
        "id": "1",
        "nombre": "Ana",
        "apellido": "Gómez",
        "email": "ana.gomez@example.com",
        "telefono": "987654321",
        "puesto": "Agente de Ventas",
        "fechaPostulacion": "2024-01-15T00:00:00",
        "apto": "si",
        "entrevista": "si",
        "estado": "finalizado"
    },
    {
        "id": "2",
        "nombre": "Carlos",
        "apellido": "Pérez",
        "email": "carlos.perez@example.com",
        "telefono": "912345678",
        "puesto": "Agente de Ventas",
        "fechaPostulacion": "2024-01-16T00:00:00",
        "apto": "no",
        "entrevista": "no",
        "estado": "finalizado"
    },
    {
        "id": "3",
        "nombre": "Laura",
        "apellido": "Martínez",
        "email": "laura.martinez@example.com",
        "telefono": "944556677",
        "puesto": "Agente de Cobranza",
        "fechaPostulacion": "2024-01-17T00:00:00",
        "apto": "si",
        "entrevista": None,
        "estado": "en_evaluacion"
    },
    {
        "id": "4",
        "nombre": "Diego",
        "apellido": "Ramírez",
        "email": "diego.ramirez@example.com",
        "telefono": "922334455",
        "puesto": "Supervisor de Turno",
        "fechaPostulacion": "2024-01-18T00:00:00",
        "apto": "si",
        "entrevista": "si",
        "estado": "finalizado"
    },
    {
        "id": "5",
        "nombre": "Sofía",
        "apellido": "Mendoza",
        "email": "sofia.mendoza@example.com",
        "telefono": "944776655",
        "puesto": "Agente de Ventas",
        "fechaPostulacion": "2024-01-19T00:00:00",
        "apto": None,
        "entrevista": None,
        "estado": "pendiente"
    }
]


def load_candidatos():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    data = [c.copy() for c in INITIAL_CANDIDATOS]
    save_candidatos(data)
    return data


def save_candidatos(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def parse_parts(path):
    return [p for p in urllib.parse.urlparse(path).path.split('/') if p]


class handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def send_cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, default=str).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        if length:
            return json.loads(self.rfile.read(length).decode('utf-8'))
        return {}

    def do_GET(self):
        parts = parse_parts(self.path)
        if len(parts) >= 2 and parts[1] == 'candidatos':
            candidatos = load_candidatos()
            if len(parts) >= 3:
                item = next((c for c in candidatos if str(c.get('id')) == parts[2]), None)
                self.send_json(item if item else {'error': 'No encontrado'}, 200 if item else 404)
            else:
                self.send_json(candidatos)
        else:
            self.send_json({'error': 'Ruta no encontrada'}, 404)

    def do_POST(self):
        parts = parse_parts(self.path)
        if len(parts) >= 2 and parts[1] == 'candidatos':
            body = self.read_body()
            body['id'] = str(uuid.uuid4())
            if not body.get('fechaPostulacion'):
                body['fechaPostulacion'] = datetime.now().isoformat()
            candidatos = load_candidatos()
            candidatos.append(body)
            save_candidatos(candidatos)
            self.send_json(body, 201)
        else:
            self.send_json({'error': 'Ruta no encontrada'}, 404)

    def do_PUT(self):
        parts = parse_parts(self.path)
        if len(parts) >= 3 and parts[1] == 'candidatos':
            item_id = parts[2]
            body = self.read_body()
            body['id'] = item_id
            candidatos = load_candidatos()
            idx = next((i for i, c in enumerate(candidatos) if str(c.get('id')) == item_id), None)
            if idx is not None:
                candidatos[idx] = body
                save_candidatos(candidatos)
                self.send_json(body)
            else:
                self.send_json({'error': 'No encontrado'}, 404)
        else:
            self.send_json({'error': 'Ruta no encontrada'}, 404)

    def do_PATCH(self):
        parts = parse_parts(self.path)
        if len(parts) >= 3 and parts[1] == 'candidatos':
            item_id = parts[2]
            body = self.read_body()
            candidatos = load_candidatos()
            idx = next((i for i, c in enumerate(candidatos) if str(c.get('id')) == item_id), None)
            if idx is not None:
                candidatos[idx].update(body)
                save_candidatos(candidatos)
                self.send_json(candidatos[idx])
            else:
                self.send_json({'error': 'No encontrado'}, 404)
        else:
            self.send_json({'error': 'Ruta no encontrada'}, 404)

    def do_DELETE(self):
        parts = parse_parts(self.path)
        if len(parts) >= 3 and parts[1] == 'candidatos':
            item_id = parts[2]
            candidatos = load_candidatos()
            new_data = [c for c in candidatos if str(c.get('id')) != item_id]
            if len(new_data) < len(candidatos):
                save_candidatos(new_data)
                self.send_json({'message': 'Eliminado'})
            else:
                self.send_json({'error': 'No encontrado'}, 404)
        else:
            self.send_json({'error': 'Ruta no encontrada'}, 404)
