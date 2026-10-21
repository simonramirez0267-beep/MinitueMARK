#!/usr/bin/env python3
"""Lee y escribe la base de la oficina (Firestore) por REST, sin dependencias.

Lo usa Claude para los correos diarios y para cargar información. Entra con la cuenta
del robot (correo y contraseña de Firebase Auth), que según las reglas puede leer y
escribir todo menos la Caja fuerte.

  python3 firestore.py leer tareas semana config            -> JSON {coleccion: {id: doc}}
  python3 firestore.py escribir cambios.json                -> aplica [{op, coleccion, id, datos}]

Credenciales por variables de entorno: OFICINA_PROYECTO, OFICINA_API_KEY,
OFICINA_ROBOT_CORREO y OFICINA_ROBOT_CLAVE. OFICINA_EMULADOR=host:puerto usa el emulador.
"""
import json, os, sys, urllib.request, urllib.parse

def a_valor(x):
    if x is None: return {'nullValue': None}
    if isinstance(x, bool): return {'booleanValue': x}
    if isinstance(x, int): return {'integerValue': str(x)}
    if isinstance(x, float): return {'doubleValue': x}
    if isinstance(x, str): return {'stringValue': x}
    if isinstance(x, list): return {'arrayValue': {'values': [a_valor(v) for v in x]}}
    if isinstance(x, dict): return {'mapValue': {'fields': {k: a_valor(v) for k, v in x.items()}}}
    raise TypeError('tipo no soportado: %r' % type(x))

def de_valor(v):
    if 'nullValue' in v: return None
    if 'booleanValue' in v: return v['booleanValue']
    if 'integerValue' in v: return int(v['integerValue'])
    if 'doubleValue' in v: return v['doubleValue']
    if 'stringValue' in v: return v['stringValue']
    if 'timestampValue' in v: return v['timestampValue']
    if 'arrayValue' in v: return [de_valor(x) for x in v['arrayValue'].get('values', [])]
    if 'mapValue' in v: return {k: de_valor(x) for k, x in v['mapValue'].get('fields', {}).items()}
    return None

class Oficina:
    def __init__(self, proyecto, api_key='', token='', emulador=''):
        host = ('http://' + emulador) if emulador else 'https://firestore.googleapis.com'
        self.raiz = '%s/v1/projects/%s/databases/(default)/documents' % (host, proyecto)
        self.nombre = 'projects/%s/databases/(default)/documents' % proyecto
        self.api_key, self.token = api_key, token

    def _pedir(self, url, cuerpo=None, metodo=None):
        if self.api_key and not self.token: url += ('&' if '?' in url else '?') + 'key=' + self.api_key
        h = {'Content-Type': 'application/json'}
        if self.token: h['Authorization'] = 'Bearer ' + self.token
        req = urllib.request.Request(url, data=json.dumps(cuerpo).encode() if cuerpo is not None else None, headers=h, method=metodo)
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read() or b'{}')

    def leer(self, coleccion):
        docs, pagina = {}, ''
        while True:
            r = self._pedir('%s/%s?pageSize=300%s' % (self.raiz, coleccion, '&pageToken=' + urllib.parse.quote(pagina) if pagina else ''))
            for d in r.get('documents', []):
                docs[d['name'].rsplit('/', 1)[1]] = {k: de_valor(v) for k, v in d.get('fields', {}).items()}
            pagina = r.get('nextPageToken', '')
            if not pagina: return docs

    def escribir(self, cambios):
        """cambios: [{op: set|update|delete, coleccion, id, datos}]; de a 400 por lote."""
        for i in range(0, len(cambios), 400):
            writes = []
            for c in cambios[i:i + 400]:
                nombre = '%s/%s/%s' % (self.nombre, c['coleccion'], c['id'])
                if c['op'] == 'delete': writes.append({'delete': nombre}); continue
                w = {'update': {'name': nombre, 'fields': {k: a_valor(v) for k, v in c['datos'].items()}}}
                if c['op'] == 'update':
                    w['updateMask'] = {'fieldPaths': ['`%s`' % k.replace('`', '\\`') for k in c['datos']]}
                    w['currentDocument'] = {'exists': True}
                writes.append(w)
            self._pedir(self.raiz + ':commit', {'writes': writes}, 'POST')

def entrar(api_key, correo, clave, emulador=''):
    host = ('http://%s/identitytoolkit.googleapis.com' % emulador) if emulador else 'https://identitytoolkit.googleapis.com'
    req = urllib.request.Request('%s/v1/accounts:signInWithPassword?key=%s' % (host, api_key),
                                 data=json.dumps({'email': correo, 'password': clave, 'returnSecureToken': True}).encode(),
                                 headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())['idToken']

def desde_entorno():
    e = os.environ
    emu = e.get('OFICINA_EMULADOR', '')
    token = entrar(e['OFICINA_API_KEY'], e['OFICINA_ROBOT_CORREO'], e['OFICINA_ROBOT_CLAVE'], e.get('OFICINA_AUTH_EMULADOR', ''))
    return Oficina(e['OFICINA_PROYECTO'], e['OFICINA_API_KEY'], token, emu)

if __name__ == '__main__':
    if len(sys.argv) < 3 or sys.argv[1] not in ('leer', 'escribir'):
        sys.exit(__doc__)
    of = desde_entorno()
    if sys.argv[1] == 'leer':
        print(json.dumps({c: of.leer(c) for c in sys.argv[2:]}, ensure_ascii=False))
    else:
        of.escribir(json.load(open(sys.argv[2])))
        print('ok')
