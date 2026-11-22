"""Pasa el Excel de cotizaciones a la sala Montaje de la Oficina.

Lee MinuteMark-Cotizaciones-Punto.xlsx (valores y fotos) y escribe montaje-oficina.json,
con el mismo formato de la copia de seguridad de la Oficina. En la Oficina:
sala Montaje › «Cargar las cotizaciones del Excel» (lo toma solo de la página),
o Historial › «Pasar datos de una copia (.json)» con este archivo.

Las fotos salen de la carpeta fotos/ (la original de cada miniatura del Excel), reducidas
a 1100 px y en JPEG, para que cada una quede muy por debajo del límite de 1 MB de Firestore.
Las ids son fijas (neveras, neveras-01, foto-...): volver a cargar actualiza, no duplica.

Uso: python3 cotizaciones/herramientas/exportar_a_oficina.py
"""
import base64, datetime, io, json, os, re
import openpyxl
from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX = os.path.join(BASE, "MinuteMark-Cotizaciones-Punto.xlsx")
FOTOS = os.path.join(BASE, "fotos")
SALIDA = os.path.join(BASE, "montaje-oficina.json")

ITEMS = ["Neveras", "Congeladores", "Estanterías", "Repisas y torre", "Mesón de pago", "Cámaras",
         "Pagos y datáfono", "Internet", "Luz y gráfica", "Estructura"]
ESTADOS = {"Por contactar": "por_contactar", "Esperando respuesta": "esperando", "Cotizado": "cotizado",
           "Negociando": "negociando", "Elegido": "elegido", "Comprado": "comprado", "Descartado": "descartado"}
IVA = {"Sí": "si", "No": "no", "No aplica": "na"}
# columnas de las hojas de ítems (fila 5 = encabezado, desde la 6 las opciones)
COL = {"proveedor": 2, "canal": 4, "contacto": 5, "zona": 6, "producto": 7, "medidas": 8, "color": 9,
       "s1": 10, "s2": 11, "s3": 12, "precio": 13, "iva": 14, "cantidad": 15, "envio": 16,
       "garantia": 18, "entrega": 19, "pago": 20, "estado": 21, "link": 22, "fecha": 23, "notas": 24}
NORMAL = {13: "Precio unitario (COP)", 15: "Cantidad", 16: "Envío e instalación (COP)", 17: "Costo total con IVA (COP)"}


def slug(t):
    t = t.lower()
    for a, b in zip("áéíóúñ", "aeioun"):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def huella(im):
    return list(im.convert("L").resize((24, 24)).tobytes())


def distancia(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) / len(a)


originales = {}
for fn in sorted(os.listdir(FOTOS)):
    with Image.open(os.path.join(FOTOS, fn)) as im:
        originales[fn] = huella(im)

fotos = {}  # id -> doc


def foto_de(img):
    """La foto original que corresponde a una miniatura del Excel; se guarda una sola vez."""
    datos = img._data()
    mini = Image.open(io.BytesIO(datos))
    fn, d = min(((f, distancia(huella(mini), h)) for f, h in originales.items()), key=lambda x: x[1])
    fuente = Image.open(os.path.join(FOTOS, fn)) if d < 400 else mini
    fid = "foto-" + (slug(fn.rsplit(".", 1)[0]) if d < 400 else "excel-%d" % len(fotos))
    if fid not in fotos:
        im = fuente.convert("RGB")
        im.thumbnail((1100, 1100))
        q = 80
        while True:
            b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True)
            if b.tell() < 260_000 or q <= 50: break
            q -= 10
        fotos[fid] = {"data": "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode(),
                      "ancho": im.width, "alto": im.height, "origen": fn if d < 400 else "Excel", "creada": AHORA}
    return fid


AHORA = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
wb = openpyxl.load_workbook(XLSX)
items, opciones = [], []
fotos_fila = {}

for n, nombre in enumerate(ITEMS):
    ws = wb[nombre]
    iid = slug(nombre)
    hdr = {c: ws.cell(5, c).value for c in range(1, 25)}
    item = {"nombre": nombre, "orden": (n + 1) * 10,
            "necesitamos": re.sub(r"^Necesitamos:\s*", "", ws["B2"].value or ""),
            "cantidad": ws["B3"].value or 1,
            "campos": {"s1": hdr[10], "s2": hdr[11], "s3": hdr[12]},
            "creado": AHORA}
    for c, defecto in NORMAL.items():
        if hdr[c] != defecto:
            item["campos"][{13: "precio", 15: "cantidad", 16: "envio", 17: "total"}[c]] = hdr[c]
    if nombre == "Estructura":
        item["tipo"] = "estructura"
    items.append({"id": iid, **item})
    por_fila = {}
    for img in ws._images:
        por_fila.setdefault(img.anchor._from.row + 1, []).append(img)
    k = 0
    for r in range(6, ws.max_row + 1):
        prov = ws.cell(r, 2).value
        if not prov:
            continue
        k += 1
        o = {"item": iid, "orden": k * 10, "creada": AHORA, "origen": "Excel"}
        for campo, c in COL.items():
            v = ws.cell(r, c).value
            if v is None or v == "":
                continue
            if campo == "estado": v = ESTADOS.get(v, v)
            elif campo == "iva": v = IVA.get(v, v)
            elif campo == "fecha": v = v.date().isoformat() if hasattr(v, "date") else str(v)
            elif campo in ("precio", "cantidad", "envio"): v = float(v) if not float(v).is_integer() else int(v)
            o[campo] = v
        o["fotos"] = [foto_de(i) for i in por_fila.get(r, [])]
        oid = "%s-%02d" % (iid, k)
        opciones.append({"id": oid, **o})
        fotos_fila[(nombre, k)] = o

# hoja Fotos: más fotos de algunas opciones («Neveras · opción 1», «Neveras · opciones 2 a 4»)
FS = wb["Fotos"]
por_fila = {}
for img in FS._images:
    por_fila.setdefault(img.anchor._from.row + 1, []).append(img)
for r in range(1, FS.max_row + 1):
    t = FS.cell(r, 1).value or ""
    m = re.match(r"(.+?) · opci[oó]n(?:es)? (\d+)(?: a (\d+))?", t)
    if not m:
        continue
    ids = [foto_de(i) for i in sorted(por_fila.get(r + 1, []), key=lambda i: i.anchor._from.col)]
    for k in range(int(m.group(2)), int(m.group(3) or m.group(2)) + 1):
        o = fotos_fila.get((m.group(1), k))
        if o is not None:
            o["fotos"] = list(dict.fromkeys(o["fotos"] + ids))

datos = {"exportado": AHORA, "origen": "cotizaciones/MinuteMark-Cotizaciones-Punto.xlsx",
         "colecciones": {"montajeItems": items, "montajeOpciones": opciones,
                         "montajeFotos": [{"id": k, **v} for k, v in fotos.items()]}}
with open(SALIDA, "w", encoding="utf-8") as f:
    json.dump(datos, f, ensure_ascii=False, separators=(",", ":"))
mayor = max(len(v["data"]) for v in fotos.values())
print("ítems %d · opciones %d · fotos %d · foto más pesada %d KB · archivo %d KB"
      % (len(items), len(opciones), len(fotos), mayor // 1024, os.path.getsize(SALIDA) // 1024))
