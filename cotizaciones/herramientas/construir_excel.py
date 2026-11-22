import datetime, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.comments import Comment

OUT = sys.argv[1]
AZUL, AZULB, HIELO, TINTA, GRIS = "0051B9", "008CFF", "E6F3FF", "0A1B33", "F1F4F8"
F = "Arial"
f_in = Font(name=F, size=10, color="0000FF")
f_calc = Font(name=F, size=10, color="000000")
f_link = Font(name=F, size=10, color="008000")
f_hdr = Font(name=F, size=10, bold=True, color="FFFFFF")
f_title = Font(name=F, size=16, bold=True, color=AZUL)
f_lbl = Font(name=F, size=10, bold=True, color=TINTA)
f_txt = Font(name=F, size=10, color=TINTA)
fill_hdr = PatternFill("solid", fgColor=AZUL)
fill_calc = PatternFill("solid", fgColor=GRIS)
fill_need = PatternFill("solid", fgColor=HIELO)
fill_key = PatternFill("solid", fgColor="FFFF00")
thin = Side(style="thin", color="D9E2EE")
box = Border(left=thin, right=thin, top=thin, bottom=thin)
wrap = Alignment(wrap_text=True, vertical="top")
COP = '$#,##0;($#,##0);"-"'

HDR_ROW, FIRST, LAST = 5, 6, 55
ESTADOS = ["Por contactar", "Esperando respuesta", "Cotizado", "Negociando", "Elegido", "Comprado", "Descartado"]
CANALES = ["Marketplace", "Fabricante", "Tienda", "Distribuidor", "Comodato", "Carpintería", "Contratista", "Operador", "Otro"]

wb = Workbook()
guide = wb.active; guide.title = "Cómo usar"
resumen = wb.create_sheet("Resumen", 0)

# ---------- Cómo usar ----------
guide.sheet_view.showGridLines = False
guide["A1"] = "MinuteMark · Cotizaciones del punto físico"; guide["A1"].font = f_title
rows = [
    ("Para qué sirve", "Una hoja por cada cosa que necesita el punto. En cada hoja van todas las opciones (proveedores) que encontremos, para comparar y tener plan B si un proveedor o un comodato se cae."),
    ("Qué se escribe", "Solo las celdas blancas con letra azul. Las grises con letra negra se calculan solas: no las borres."),
    ("Precio", "Escribe el precio tal cual te lo dieron y marca en '¿IVA incluido?' si lo incluye. Si dices 'No', el costo total le suma el IVA para comparar parejo. Marketplace sin factura: 'No aplica'."),
    ("Cantidad", "Si la dejas vacía, se usa la cantidad que necesita el punto (celda B3 de cada hoja)."),
    ("Estado", "Cuando escojamos una opción, márcala 'Elegido' (o 'Comprado' si ya la tenemos). El Resumen toma esa. Si no hay ninguna elegida, el Resumen usa la más barata como presupuesto."),
    ("Fotos", "Cada opción lleva su foto en la columna C, al lado del proveedor. Para poner una tú: selecciona la celda de la columna Foto y usa Insertar > Imágenes > Colocar en celda. Si hay varias fotos de la misma opción, van en la hoja Fotos."),
    ("Puntos", "Cuando se monte un punto, en la hoja Puntos se anota cada equipo y mueble que quedó: proveedor, contacto, fecha, valor y meses de garantía. El Excel calcula cuándo vence la garantía y avisa si está vencida o vence en menos de 30 días."),
    ("Estructura", "En la hoja Estructura cada fila es un componente (muros, techo, piso, eléctrico...). En 'Aplica a' indica si sirve para parqueadero en sótano, al aire libre o ambos. El Resumen arma los dos escenarios."),
]
r = 3
for k, v in rows:
    guide.cell(r, 1, k).font = f_lbl; guide.cell(r, 2, v).font = f_txt; guide.cell(r, 2).alignment = wrap
    guide.row_dimensions[r].height = 42; r += 1
r += 1
guide.cell(r, 1, "IVA").font = f_lbl
c = guide.cell(r, 2, 0.19); c.font = f_in; c.number_format = "0%"; c.fill = fill_key
c.comment = Comment("Tarifa general de IVA en Colombia. Se usa cuando el precio cotizado no lo incluye.", "MinuteMark")
iva_row = r
wb.defined_names["IVA"] = DefinedName("IVA", attr_text=f"'Cómo usar'!$B${iva_row}")
r += 2
guide.cell(r, 1, "Ejemplo de una fila llena (inventado, solo para ver el formato)").font = f_lbl; r += 1
ex_h = ["Proveedor", "Canal", "Contacto", "Producto", "Medidas", "Color", "Precio unitario", "¿IVA incluido?", "Garantía", "Entrega", "Forma de pago", "Estado"]
ex_v = ["Refrigeración del Valle (ejemplo)", "Marketplace", "Andrés · 300 000 0000", "Nevera vertical 1 puerta 400 L", "65 × 65 × 200 cm", "Blanca, sin logos", 2350000, "No aplica", "6 meses", "3 días", "Contra entrega", "Cotizado"]
for i, (h, v) in enumerate(zip(ex_h, ex_v)):
    a = guide.cell(r, 1 + i, h); a.font = f_hdr; a.fill = fill_hdr; a.alignment = wrap
    b = guide.cell(r + 1, 1 + i, v); b.font = f_in; b.border = box; b.alignment = wrap
    if isinstance(v, int): b.number_format = COP
guide.column_dimensions["A"].width = 24; guide.column_dimensions["B"].width = 95
for col in "CDEFGHIJKL": guide.column_dimensions[col].width = 16

# ---------- item sheets ----------
COLS = ["#", "Proveedor", "Foto", "Canal", "Contacto (nombre y WhatsApp)", "Zona / ciudad", "Producto o referencia",
        "Medidas (frente × fondo × alto)", "Color / ¿se puede brandear?", "S1", "S2", "S3",
        "Precio unitario (COP)", "¿IVA incluido?", "Cantidad", "Envío e instalación (COP)", "Costo total con IVA (COP)",
        "Garantía", "Tiempo de entrega", "Forma de pago", "Estado", "Link", "Fecha de cotización", "Notas"]
WID = [4, 22, 24, 13, 24, 16, 30, 20, 20, 14, 14, 14, 15, 11, 9, 14, 16, 12, 13, 16, 15, 30, 12, 40]

from openpyxl.drawing.image import Image as XLImage
from openpyxl.drawing.spreadsheet_drawing import TwoCellAnchor, AnchorMarker
from PIL import Image as PImage
import os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(BASE, "fotos") + "/"
import tempfile
TH = os.path.join(tempfile.gettempdir(), "mm-thumbs") + "/"
os.makedirs(TH, exist_ok=True)
EMU = 9525
BOX_W, BOX_H = 165, 154   # px usable in column C (24 chars) and a 120 pt row

def thumb(fn, maxpx=600):
    im = PImage.open(IMG + fn).convert("RGB"); im.thumbnail((maxpx, maxpx))
    out = TH + fn.rsplit(".", 1)[0] + ".jpg"; im.save(out, "JPEG", quality=85)
    return out, im.size

def put_photo(ws, row, fn):
    """Photo inside column C of `row`, centered, kept in proportion, moves and sorts with the row."""
    path, (w, h) = thumb(fn)
    sc = min(BOX_W / w, BOX_H / h); dw, dh = int(w * sc), int(h * sc)
    ox, oy = (173 - dw) // 2, (160 - dh) // 2
    xi = XLImage(path); xi.width, xi.height = dw, dh
    xi.anchor = TwoCellAnchor(editAs="twoCell",
        _from=AnchorMarker(col=2, colOff=ox * EMU, row=row - 1, rowOff=oy * EMU),
        to=AnchorMarker(col=2, colOff=(ox + dw) * EMU, row=row - 1, rowOff=(oy + dh) * EMU))
    ws.add_image(xi)
    ws.row_dimensions[row].height = 120

def item_sheet(name, need, qty, specs, rows=(), price_hdr=None, qty_hdr=None, inst_hdr=None, total_hdr=None):
    ws = wb.create_sheet(name)
    ws.sheet_view.showGridLines = False
    ws["A1"] = name; ws["A1"].font = f_title
    ws["B2"] = "Necesitamos: " + need; ws["B2"].font = f_lbl
    ws["B3"] = qty; ws["B3"].font = f_in; ws["B3"].fill = fill_need
    ws["C3"] = "← cantidad que necesita el punto (se usa si la fila no dice otra cantidad)"; ws["C3"].font = Font(name=F, size=9, italic=True, color="5B6B82")
    hdr = list(COLS); hdr[9:12] = specs
    if price_hdr: hdr[12] = price_hdr
    if qty_hdr: hdr[14] = qty_hdr
    if inst_hdr: hdr[15] = inst_hdr
    if total_hdr: hdr[16] = total_hdr
    for i, h in enumerate(hdr, 1):
        c = ws.cell(HDR_ROW, i, h); c.font = f_hdr; c.fill = fill_hdr; c.alignment = Alignment(wrap_text=True, vertical="center"); c.border = box
        ws.column_dimensions[c.column_letter].width = WID[i - 1]
    ws.row_dimensions[HDR_ROW].height = 42
    for rr in range(FIRST, LAST + 1):
        for i in range(1, len(hdr) + 1):
            c = ws.cell(rr, i); c.border = box; c.alignment = wrap; c.font = f_in
        ws.cell(rr, 1, f'=IF(B{rr}="","",ROW()-{FIRST-1})').font = f_calc
        ws.cell(rr, 1).fill = fill_calc
        p = ws.cell(rr, 17, f'=IF(M{rr}="","",IF(N{rr}="No",M{rr}*(1+IVA),M{rr})*IF(O{rr}="",$B$3,O{rr})+N(P{rr}))')
        p.font = f_calc; p.fill = fill_calc; p.number_format = COP
        ws.cell(rr, 13).number_format = COP; ws.cell(rr, 16).number_format = COP
        ws.cell(rr, 23).number_format = "dd/mm/yyyy"
    for j, row in enumerate(rows):
        rr = FIRST + j
        for col, val in row.items():
            if col == "foto": continue
            ws.cell(rr, col + 1 if col >= 3 else col, val)
    rng = lambda L: f"{L}{FIRST}:{L}{LAST}"
    for formula, col in [('"' + ",".join(ESTADOS) + '"', "U"), ('"Sí,No,No aplica"', "N"), ('"' + ",".join(CANALES) + '"', "D")]:
        dv = DataValidation(type="list", formula1=formula, allow_blank=True); ws.add_data_validation(dv); dv.add(rng(col))
    ws.freeze_panes = "D6"
    ws.auto_filter.ref = f"A{HDR_ROW}:X{LAST}"
    for j, row in enumerate(rows):
        if row.get("foto"):
            put_photo(ws, FIRST + j, row["foto"])
    return ws

D = datetime.date(2026, 11, 19)
sheets = []
D2 = datetime.date(2026, 11, 21)
PROV = "Frozentech"
nev_common = {2: PROV, 3: "Marketplace", 4: "Pedir WhatsApp y nombre del asesor", 5: "Valle de Aburrá", 13: "No aplica", 15: 0,
              18: "Envío gratis Bello–Caldas", 19: "Contra entrega", 20: "Cotizado", 22: D2}
nev_rows = [
    {**nev_common, **{6: "Nevera exhibidora 2 puertas de vidrio, luz LED, solo refrigeración (Indufrial en las fotos)",
        7: "100 × ? × 200 cm (fondo por confirmar)", 8: "Negra, azul o plateada según unidad; quitar logos de marcas", 9: "2 puertas", 10: "Por confirmar",
        11: "Usada o reacondicionada (confirmar)", 12: 4000000, 14: 1, 17: "4 meses (sistema de enfriamiento)", "foto": "nevera-frozentech-2p-a.webp",
        21: "Más fotos en la hoja Fotos",
        23: "Precio 'desde': pedir el valor de la unidad exacta. Una sola de 2 puertas (1,00 m) reemplaza las 2 neveras del 3D (1,30 m) y libera espacio. "
            "La foto azul tiene stickers 'Equipo para baja' y 'propiedad de Postobón S.A.': pedir factura o documento que pruebe que el equipo es del vendedor."}},
    {**nev_common, **{6: "Nevera exhibidora panorámica 1 puerta, luz LED, solo refrigeración", 7: "? × ? × 150 cm", "foto": "nevera-frozentech-1p-a.webp",
        8: "Varias; marcos con logos de marcas", 9: "1 puerta", 10: "Por confirmar", 11: "Usada o reacondicionada (confirmar)", 12: 1300000,
        17: "4 meses (sistema de enfriamiento)", 21: "Foto de referencia. Más en la hoja Fotos",
        23: "1,50 m queda baja frente al 3D (2,00 m): se pierde exhibición en altura."}},
    {**nev_common, **{6: "Nevera exhibidora panorámica 1 puerta, luz LED, solo refrigeración", 7: "? × ? × 180 cm", "foto": "nevera-frozentech-1p-a.webp",
        8: "Varias; marcos con logos de marcas", 9: "1 puerta", 10: "Por confirmar", 11: "Usada o reacondicionada (confirmar)",
        17: "4 meses (sistema de enfriamiento)", 20: "Esperando respuesta", 21: "Foto de referencia. Más en la hoja Fotos",
        23: "No dio precio: está entre $1,3 M y $1,9 M. Pedirlo."}},
    {**nev_common, **{6: "Nevera exhibidora panorámica 1 puerta, luz LED, solo refrigeración", 7: "? × ? × 200 cm", "foto": "nevera-frozentech-1p-b.webp",
        8: "Varias; marcos con logos de marcas (Pony Malta, Poker, Fogel, Imbera)", 9: "1 puerta", 10: "Por confirmar", 11: "Usada o reacondicionada (confirmar)",
        12: 1900000, 17: "4 meses (sistema de enfriamiento)", 21: "Foto de referencia. Más en la hoja Fotos",
        23: "Es la medida del 3D. Dos de estas cuestan casi lo mismo que una de 2 puertas, con dos compresores: si una falla, la otra sigue enfriando."}},
]
sheets.append((item_sheet("Neveras", "Neveras verticales de 0,65 × 0,65 × 2,00 m (o una de 2 puertas de hasta 1,40 m de ancho). Ideal blancas o azules, sin logo de gaseosa, para vestirlas con la marca.", 2,
    ["Tipo (puertas)", "Capacidad (litros)", "Nueva / usada"], nev_rows), "Neveras verticales"))
sheets.append((item_sheet("Congeladores", "Congeladores horizontales con tapa de vidrio de 1,00 × 0,70 × 0,85 m (helados y congelados).", 2,
    ["Capacidad (litros)", "Tapa de vidrio", "Nuevo / usado"]), "Congeladores"))
HC = "https://www.homecenter.com.co/homecenter-co/product/"
ec = {13: "Sí", 22: D2}
est_rows = [
    {**ec, 2: "Homecenter (RTA Muebles)", 3: "Tienda", 5: "Medellín", 6: "Estante Home E3, 5 espacios, código 656368 (también se vende en set de 4 unidades)",
     7: "62,8 × 29,9 × 180,6 cm", 8: "Blanco", 9: "5 espacios", 10: "Pedir", 11: "Aglomerado con melamina", 12: 249900, "foto": "estanteria-homecenter-656368.jpg",
     20: "Cotizado", 21: HC + "656368/estante-home-e3-5-espacios-180-x-62cm-rta-blanco-set-x-4-unidades/778301/",
     23: "Medida exacta. Precio en la página el 22 nov: $249.900 (en julio estaba en $299.900). El set de 4 son justo los 4 módulos: pedir precio del set."},
    {**ec, 2: "Homecenter (RTA Muebles)", 3: "Tienda", 5: "Medellín", 6: "Combo Home blanco, 2 bibliotecas sin puertas, código 666936",
     7: "62 × 29 × 180 cm (cada una)", 8: "Blanco", 9: "5 espacios", 10: "Pedir", 11: "Aglomerado con melamina", 12: 344950, "foto": "estanteria-homecenter-666936.jpg",
     20: "Cotizado", 21: HC + "666936/combo-home-180x62x29cm-blanco-dos-bibliotecas/666936/",
     23: "Precio por unidad: el combo de 2 cuesta $689.900 (página, 22 nov)."},
    {**ec, 2: "Homecenter (RTA Muebles)", 3: "Tienda", 5: "Medellín", 6: "Combo Home blanco, 3 bibliotecas sin puertas, código 661539",
     7: "62 × 29 × 180 cm (cada una)", 8: "Blanco", 9: "5 espacios", 11: "Aglomerado con melamina", 12: 366633, 13: "Sí", "foto": "estanteria-homecenter-661539.jpg",
     20: "Cotizado", 21: HC + "661539/combo-home-blanco-3-bibliotecas-sin-puertas/661539/", 23: "El combo de 3 cuesta $1.099.900 (página, 22 nov); aquí va por unidad. Ojo: en la foto el módulo del centro tiene puertas abajo, aunque el nombre dice sin puertas."},
    {**ec, 2: "Homecenter (Virtual Muebles)", 3: "Tienda", 5: "Medellín", 6: "Biblioteca Home 180 × 63 × 30",
     7: "62,8 × 29,9 × 180,6 cm", 8: "Macadamia (madera clara)", 9: "4 repisas", 10: "Pedir", 11: "Aglomerado con melamina", 12: 359900, "foto": "estanteria-homecenter-661545.jpg",
     20: "Cotizado", 21: "https://homecenter.falabella.com.co/homecenter-co/product/140562805",
     23: "Precio en la página el 22 nov: $359.900 (normal $529.900)."},
    {**ec, 2: "Éxito (vendedor RTA)", 3: "Tienda", 5: "Envío a Medellín", 6: "Biblioteca Home, 5 entrepaños",
     7: "62,8 × 29,9 × 180,6 cm (confirmar)", 8: "Milán y blanco duqueza (madera + blanco)", 9: "5", 10: "Pedir", 11: "Aglomerado con melamina", 12: 349900,
     20: "Cotizado", 21: "https://www.exito.com/biblioteca-home-milan-y-blanco-duqueza-con-cinco-entrepanos-104745535-mp/p",
     23: "Precio con descuento (normal $491.900). Confirmar medidas en la ficha."},
    {**ec, 2: "Éxito (vendedor RTA)", 3: "Tienda", 5: "Envío a Medellín", 6: "Biblioteca Home, 5 entrepaños",
     7: "62,8 × 29,9 × 180,6 cm (confirmar)", 8: "Avellana y wengue (madera oscura)", 9: "5", 11: "Aglomerado con melamina", "foto": "estanteria-rta-home-wengue.jpg",
     20: "Por contactar", 21: "https://www.exito.com/biblioteca-home-avellana-y-wengue-con-cinco-entrepanos-104962835-mp/p", 23: "No apareció el precio (Éxito bloquea la consulta automática). Foto de referencia del fabricante en wengue."},
    {**ec, 2: "Homecenter", 3: "Tienda", 5: "Medellín", 6: "Estantería biblioteca Multy, código 360880",
     7: "60 × 30 × 180 cm", 8: "Blanco", 9: "5", 10: "20 kg", 11: "Madera aglomerada", 12: 379900, "foto": "estanteria-homecenter-360880.jpg",
     20: "Cotizado", 21: HC + "360880/estanteria-biblioteca-multy-180x60x30-blanco/360880/",
     23: "3 cm más angosta. La única con carga publicada aceptable (20 kg por repisa). Precio en la página el 22 nov: $379.900."},
    {**ec, 2: "Homecenter", 3: "Tienda", 5: "Medellín", 6: "Estantería librero biblioteca en MDP 60 cm, código 688708",
     7: "60 × 30 × 180 cm", 8: "Negro", 9: "4", 10: "5 kg", 11: "MDP", 12: 619900, "foto": "estanteria-homecenter-688708.jpg",
     20: "Cotizado", 21: HC + "688708/estanteria-librero-biblioteca-en-mdp-60cm-4-estantes-negro/688708/",
     23: "Única negra con la medida, pero aguanta 5 kg por repisa: no sirve para gaseosas ni aceite. Cara para lo que es."},
    {**ec, 2: "Homecenter", 3: "Tienda", 5: "Medellín", 6: "Biblioteca librero en MDP 60 cm, 5 estantes, código 718067",
     7: "60 × 30 × 180 cm", 8: "Menta", 9: "5", 10: "Pedir", 11: "MDP", 12: 297900, "foto": "estanteria-homecenter-718067.jpg",
     20: "Cotizado", 21: HC + "718067/biblioteca-estanteria-librero-en-mdp-60cm-5-estantes-menta/718067/",
     23: "Precio en la página el 22 nov: $297.900. Color menta, no es de la marca."},
    {2: "Colombia Move (usada)", 3: "Marketplace", 5: "El Peñol, Antioquia", 6: "Biblioteca estantería de 5 niveles, armada",
     7: "63 × 30 × 180 cm", 8: "No dice", 9: "5", 12: 200000, 13: "No aplica", 20: "Por contactar", 22: D2,
     21: "https://colombiamove.com/anuncio/biblioteca-estanteria-librero-de-5-niveles-180-cm-de-alto-611b66ce",
     23: "Medida exacta, negociable, pero es una sola unidad y está en El Peñol."},
    {**ec, 2: "Homecenter (RTA Muebles)", 3: "Tienda", 5: "Medellín", 6: "Combo Home wengue, 3 bibliotecas, código 666923",
     7: "62 × 29 × 180 cm (cada una)", 8: "Wengue (café tan oscuro que se ve casi negro)", 9: "5 espacios", 11: "Aglomerado con melamina", "foto": "estanteria-rta-home-wengue.jpg",
     20: "Por contactar", 21: HC + "666923/combo-home-180x62x29cm-wengue-tres-bibliotecas/666923/",
     23: "La opción oscura con la medida exacta. Foto del fabricante (RTA). Pedir precio y confirmar que vengan sin puertas."},
    {2: "RTA Muebles (fabricante de la línea Home)", 3: "Fabricante", 5: "Colombia", 6: "Línea Estantería Home 180,6 × 62,8 × 29,9",
     7: "62,8 × 29,9 × 180,6 cm", 8: "Blanco, wengue (casi negro), macadamia y blanco", 11: "Aglomerado con melamina", 20: "Por contactar", 22: D2, "foto": "estanteria-rta-home-blanco.jpg",
     21: "https://www.rta.com.co/categorias/bibliotecas-oficinas/",
     23: "Son los que fabrican el formato. Preguntar: precio por volumen para varios puntos, si los entrepaños son graduables (sus manuales traen soportes de entrepaño) y carga por entrepaño."},
    {2: "Muebles Bika", 3: "Carpintería", 5: "Medellín", 6: "Módulo a medida 63 × 30 × 180 en melamina, entrepaños graduables",
     7: "63 × 30 × 180 cm", 8: "Cualquier color de su carta (9 colores)", 9: "Graduables", 11: "Melamina 18 mm", 20: "Por contactar", 22: D2,
     21: "https://bika.com.co/muebles-personalizados-a-medida-en-bika/",
     23: "Única ruta encontrada para azul o gris. Pedir melamina de 18 mm y entrepaño reforzado. Cobran $238.000 la visita de medidas a empresas."},
]
sheets.append((item_sheet("Estanterías", "Módulo universal MinuteMark: 1,80 m de alto (mínimo) × 63 cm de ancho × 30 cm de fondo, entrepaños graduables (ej. para gaseosas de 3 L). Madera o melamina, nada industrial. Colores: blanco, azul, gris o negro. Regla: ancho 60–66, fondo 28–32 y alto 180–185 cm; lo que no cumpla no entra. En la pared de 2,94 m caben 4.", 4,
    ["Entrepaños", "Carga por entrepaño", "Material"], est_rows), "Estanterías (módulo 180 × 63 × 30)"))
sheets.append((item_sheet("Repisas y torre", "2 repisas de pared de 1,00 × 0,30 m con 3 niveles (sobre congeladores) y 1 torre de esquina de 0,59 × 0,60 × 2,20 m. Indica en 'Cantidad' cuántas de cada una.", 3,
    ["Tipo (repisa / torre)", "Niveles", "Material"]), "Repisas de pared y torre"))
meson_rows = [
    {**ec, 2: "Homecenter (RTA Muebles)", 3: "Tienda", 5: "Medellín", 6: "Opción A · Módulo universal convertido en punto de pago (Estante Home E3, código 656368)",
     7: "62,8 × 29,9 × 180,6 cm", 8: "Blanco", 9: "Aglomerado con melamina", 10: "Un entrepaño a 1 m como mesa", 11: "Cenefa azul + vinilo de Mark",
     12: 249900, "foto": "estanteria-homecenter-656368.jpg", 20: "Cotizado",
     21: HC + "656368/estante-home-e3-5-espacios-180-x-62cm-rta-blanco-set-x-4-unidades/778301/",
     23: "Como en el punto de Always Smart: un módulo sin entrepaños en la zona de pago. Se deja uno a 1 m de alto para el datáfono, arriba productos de impulso (chicles, chocolatinas) y la cámara encima. Es el mismo mueble de las estanterías: todo se ve igual y ordenado. Ojo: 30 cm de fondo alcanza para el datáfono y apoyar 2 o 3 productos."},
    {2: "Muebles Bika", 3: "Carpintería", 5: "Medellín", 6: "Opción B · Mesón de pago a medida", 7: "80 × 50 × 100 cm (medida del 3D)",
     8: "Blanco con frente azul", 9: "Melamina 18 mm", 10: "Cajón o puerta abajo", 11: "Frente con logo",
     20: "Por contactar", 22: D2, 21: "https://bika.com.co/muebles-personalizados-a-medida-en-bika/",
     23: "Más espacio para apoyar la compra y frente para poner la marca. Más caro y hay que esperar fabricación."},
]
sheets.append((item_sheet("Mesón de pago", "Punto de pago para el datáfono y la cámara. Dos caminos: el mismo módulo de estantería sin entrepaños (como el punto de Always Smart) o un mesón propio de 0,80 × 0,50 × 1,00 m.", 1,
    ["Material", "Superficie de pago", "Acabado"], meson_rows), "Mesón de pago"))
FAL = "https://www.falabella.com.co/falabella-co/"
cc = {3: "Tienda", 5: "Envío a Medellín", 13: "Sí", 20: "Cotizado", 22: D2}
cam_rows = [
    {2: "Ya compradas (completar dónde)", 3: "Tienda", 6: "TP-Link Tapo C110 · las del primer punto", 8: "Blanca", "foto": "camara-tapo-c110.jpg", 9: "3 MP (2304 × 1296)",
     10: "microSD hasta 256 GB + nube Tapo Care (opcional)", 11: "App Tapo", 12: 99900, 13: "Sí", 20: "Comprado", 22: D2,
     21: "https://www.alkosto.com/camara-seguridad-interior-fija-tp-link-tapo-c110-wifi-2k/p/840030702761",
     23: "Fija (no gira), visión nocturna ~9 m, audio de doble vía, solo wifi de 2,4 GHz. Precio de referencia de Alkosto: cambiar por lo que pagaron y anotar cuántas son."},
    {**cc, 2: "Alkosto", 5: "Medellín", 6: "TP-Link Tapo C110 (la misma)", 8: "Blanca", "foto": "camara-tapo-c110.jpg", 9: "3 MP (2304 × 1296)", 10: "microSD hasta 256 GB + Tapo Care", 11: "App Tapo",
     12: 99900, 21: "https://www.alkosto.com/camara-seguridad-interior-fija-tp-link-tapo-c110-wifi-2k/p/840030702761",
     23: "Precio confirmado en la página el 22 nov: $99.900 (normal $129.900). Repetir la misma cámara en cada punto deja todo en una sola app."},
    {**cc, 2: "Falabella", 6: "TP-Link Tapo C110 · paquete de 2", 8: "Blanca", "foto": "camara-tapo-c110.jpg", 9: "3 MP (2304 × 1296)", 10: "microSD hasta 256 GB + Tapo Care", 11: "App Tapo",
     12: 119950, 21: FAL + "brand/TAPO", 23: "El paquete de 2 cuesta $239.900; aquí va el precio por cámara."},
    {**cc, 2: "Falabella", 6: "TP-Link Tapo C220 2K QHD, gira 360°", 8: "Blanca", "foto": "camara-tapo-c220.jpg", 9: "4 MP (2560 × 1440)", 10: "microSD + Tapo Care", 11: "App Tapo",
     12: 154900, 21: FAL + "product/150460226/camara-de-seguridad-wifi-tp-link-tapo-c220-2k-qhd/150460227",
     23: "Más nitidez que la C110 y detección con IA. Precio normal $178.200. Gira: con una sola se cubre casi todo el punto."},
    {**cc, 2: "Homecenter", 5: "Medellín", 6: "TP-Link Tapo C210 2K, gira 360°", 8: "Blanca", "foto": "camara-tapo-c210.jpg", 9: "3 MP", 10: "microSD + Tapo Care", 11: "App Tapo",
     12: 89900, 21: "https://www.falabella.com.co/falabella-co/category/CATG33327/Camaras-CCTV",
     23: "La más barata que gira. En Falabella hay paquete de 2 por $181.900. Confirmar precio en Homecenter."},
    {**cc, 2: "Falabella", 6: "TP-Link Tapo C225 2K, gira 360° con seguimiento", 8: "Blanca", "foto": "camara-tapo-c225.png", 9: "4 MP (2K)", 10: "microSD + Tapo Care", 11: "App Tapo",
     12: 197910, 21: FAL + "brand/TAPO", 23: "La más completa de Tapo en esta lista. Precio de referencia $458.000."},
    {**cc, 2: "Falabella (vendedor Ezviz)", 6: "Ezviz H6c 2K, gira 360°", 8: "Blanca", "foto": "camara-ezviz-h6c.jpg", 9: "3 MP (2K)", 10: "microSD + nube Ezviz", 11: "App Ezviz",
     12: 120900, 21: FAL + "brand/EZVIZ", 23: "Otra app distinta a la de las C110: obliga a manejar dos apps."},
    {**cc, 2: "Falabella", 6: "Imou Ranger Mini, gira, detección humana con IA", 8: "Blanca", "foto": "camara-imou-ranger-mini.jpg", 9: "3 MP", 10: "microSD + nube Imou", 11: "App Imou",
     12: 139899, 21: "https://www.falabella.com.co/falabella-co/product/149925488/camara-de-seguridad-ranger-mini-imou-3mp-wifi-full-color-deteccion-humana-ia-audio-2-vias",
     23: "Visión nocturna a color. Precio normal $180.000. Otra app distinta."},
    {2: "Tapo Care (nube de TP-Link)", 3: "Operador", 5: "En la app Tapo", 6: "Suscripción para guardar los videos en la nube", 11: "App Tapo",
     20: "Por contactar", 22: D2, 21: "https://tapo.com/es/faqs/general-questions-about-tapo-care",
     23: "SERVICIO: se suma a las cámaras. Si se roban la cámara o la memoria, el video queda en la nube. Referencia (no es precio de Colombia): Básico desde USD 3,49 al mes por cámara. Ver el precio real en la app: Yo › Tapo Care."},
]
sheets.append((item_sheet("Cámaras", "Cámaras para el punto: ver el mesón de pago y todo el pasillo, con grabación que no se pierda si se roban la cámara. Ya hay Tapo C110 compradas para el primer punto.", 2,
    ["Resolución", "Almacenamiento", "App / nube"], cam_rows), "Cámaras"))
sheets.append((item_sheet("Pagos y datáfono", "Datáfono o sistema de pago con tarjeta y QR.", 1,
    ["Comisión por venta (%)", "Mensualidad", "Acepta QR / Nequi"]), "Datáfono"))
SOMOS = "https://www.somosinternet.com/planes-medellin"
sc = {2: "Somos Internet", 3: "Operador", 4: "WhatsApp desde la página", 5: "Medellín y Valle de Aburrá", 10: "Fibra activa simétrica", 11: "Sin permanencia",
      18: "Prueba 30 días gratis", 20: "Cotizado", 21: SOMOS, 22: D2}
inet_rows = [
    {**sc, 6: "Plan Essential · estratos 1, 2 y 3", 9: "Hasta 900", 12: 63000, 13: "No aplica", "foto": "internet-somos-estratos-1-3.webp",
     23: "2 puntos cableados, hasta 2 routers, Orb 2 no incluido, soporte 24/7. Estratos 1 a 3 no pagan IVA en internet residencial."},
    {**sc, 6: "Plan Pro · estratos 1, 2 y 3", 9: "Hasta 2.000", 12: 100000, 13: "No aplica", "foto": "internet-somos-estratos-1-3.webp",
     23: "Puntos cableados ilimitados, los routers necesarios, 1 Orb 2 incluido, soporte VIP 24/7."},
    {**sc, 6: "Plan Essential · estratos 4, 5 y 6", 9: "Hasta 900", 12: 75000, 13: "Sí", "foto": "internet-somos-estratos-4-6.webp",
     23: "Lo mismo del Essential de estratos 1 a 3, con IVA incluido."},
    {**sc, 6: "Plan Pro · estratos 4, 5 y 6", 9: "Hasta 2.000", 12: 120000, 13: "Sí", "foto": "internet-somos-estratos-4-6.webp",
     23: "Según Simón, es el que usa Always Smart en el edificio Flats (en celda de parqueadero). Preguntar qué es el Orb 2: si es respaldo ante cortes de luz, justifica pagar el Pro."},
    {2: "Movistar", 3: "Operador", 5: "Medellín", 6: "Fibra óptica 900 Mbps", 9: "900", 10: "Fibra GPON (no simétrica)", 11: "Confirmar",
     12: 94990, 13: "Sí", 20: "Cotizado", 21: "https://selectra.com.co/internet-hogar/medellin", 22: D2,
     23: "$75.992 los primeros 6 meses y después $94.990 (dato de comparador). Opensignal: Movistar es el mejor del país; en Medellín gana Somos."},
    {2: "Claro", 3: "Operador", 5: "Medellín", 6: "Internet fibra 900 Mbps", 9: "900", 10: "Fibra GPON o cable HFC según la zona", 11: "Confirmar",
     12: 89900, 13: "Sí", 20: "Cotizado", 21: "https://compraclaro.com/hogarmedellin", 22: D2,
     23: "Precio de lista sin promoción. Hay combos con TV desde $49.950 los primeros meses que después suben a $99.900. Confirmar que en la dirección sea fibra y no cable."},
    {2: "Velonet", 3: "Operador", 4: "+57 300 910 9110", 5: "Medellín", 6: "Internet hogar fibra óptica", 9: "Hasta 1.000", 10: "Fibra óptica",
     11: "Algunas ofertas: 12 meses", 20: "Por contactar", 21: "https://webcolombia.velonet.co/", 22: D2,
     23: "Operador paisa. Opensignal lo pone empatado en calidad constante con Claro y Tigo en Medellín. Ojo: algunas ofertas cobran $500.000 de conexión con permanencia de 12 meses."},
    {2: "Respaldo 4G (router con SIM)", 3: "Tienda", 5: "Medellín", 6: "Router con SIM y cambio automático a datos móviles si se cae la fibra (ej. TP-Link Archer MR600 u Omada ER706W-4G) + plan de datos",
     9: "Hasta 300 (4G)", 10: "4G LTE", 11: "Prepago: sin permanencia", 20: "Por contactar", 22: D2,
     23: "RESPALDO: se suma al plan de fibra, no lo reemplaza. Si la fibra se cae, las cámaras y el datáfono siguen funcionando. Cotizar el router y una SIM de datos."},
    {2: "UPS para router", 3: "Tienda", 5: "Medellín", 6: "UPS pequeña o batería DC para router y equipo de fibra", 10: "Respaldo de energía",
     20: "Por contactar", 22: D2, 23: "RESPALDO: mantiene el internet prendido en un corte de luz. Funciona solo si el operador tiene batería en su red."},
    {2: "Starlink", 3: "Operador", 5: "Colombia", 6: "Residencial Lite (satelital)", 9: "Variable", 10: "Satelital", 11: "Confirmar",
     12: 150000, 13: "Sí", 20: "Cotizado", 21: "https://www.enter.co/?p=581318", 22: D2,
     23: "Solo para un punto sin fibra o como respaldo en parqueadero al aire libre: necesita ver el cielo y no sirve en sótano. Equipo aparte: $800.000 a $1.599.000. Promoción de $89.999 el primer año."},
]
sheets.append((item_sheet("Internet", "Internet de fibra para cámaras, datáfono y pantalla. Con 100 a 300 Mbps sobra (las cámaras suben unos 2 a 4 Mbps cada una). Lo que importa es que no se caiga: fibra + respaldo 4G + UPS. Tigo queda descartado.", 12,
    ["Velocidad (Mbps)", "Fibra / inalámbrico", "Cláusula de permanencia"], inet_rows,
    price_hdr="Precio mensual (COP)", qty_hdr="Meses", inst_hdr="Instalación (COP)", total_hdr="Costo primer año (COP)"), "Internet (primer año)"))
sheets.append((item_sheet("Luz y gráfica", "Tira LED con perfil bajo cada entrepaño (~18 m), cenefa azul (~18 m), 6 avisos de categoría, zócalo y vinilos de Mark. Una fila por ítem.", 1,
    ["Ítem (LED, cenefa, aviso...)", "Metros / unidades", "Temperatura de luz"]), "Luz LED y gráfica"))

# ---------- Estructura ----------
COMPS = ["Cerramiento (muros)", "Techo / cubierta", "Piso", "Fachada y puerta", "Eléctrico y acometida", "Iluminación general",
         "Ventilación", "Impermeabilización y desagüe", "Gráfica exterior", "Montaje llave en mano", "Permisos y pólizas"]
REF = {"Cerramiento (muros)": "$3 – 6 M", "Techo / cubierta": "Por cotizar (solo aire libre)", "Piso": "$0,5 – 1 M", "Fachada y puerta": "$2,5 – 6 M",
       "Eléctrico y acometida": "$2 – 4 M", "Iluminación general": "Por cotizar", "Ventilación": "$0,5 – 1,5 M",
       "Impermeabilización y desagüe": "Por cotizar", "Gráfica exterior": "$1 – 2,5 M", "Montaje llave en mano": "Reemplaza varias filas", "Permisos y pólizas": "Por cotizar"}
ws = item_sheet("Estructura", "Lo que hay que construir si el punto va en una celda de parqueadero (sótano o al aire libre como Bosques de la Cascada). Una fila por componente y proveedor.", 1,
    ["Componente", "Aplica a", "Material"])
for col, lst in [("J", COMPS), ("K", ["Ambos", "Sótano", "Aire libre"])]:
    dv = DataValidation(type="list", formula1='"' + ",".join(lst) + '"', allow_blank=True); ws.add_data_validation(dv); dv.add(f"{col}{FIRST}:{col}{LAST}")
ws.cell(4, 10, "Si 'Aplica a' queda vacío se cuenta para los dos escenarios.").font = Font(name=F, size=9, italic=True, color="5B6B82")
bh = ["Componente", "Más barata · sótano", "Más barata · aire libre", "Elegida · sótano", "Elegida · aire libre", "Referencia informe 19 nov (estimado)"]
B0 = 26  # column Z
for i, h in enumerate(bh):
    c = ws.cell(HDR_ROW, B0 + i, h); c.font = f_hdr; c.fill = PatternFill("solid", fgColor=TINTA); c.alignment = Alignment(wrap_text=True, vertical="center"); c.border = box
    ws.column_dimensions[c.column_letter].width = 18 if i else 28
ws.column_dimensions["Y"].width = 3
P, I_, J, T = (f"$Q${FIRST}:$Q${LAST}", f"$J${FIRST}:$J${LAST}", f"$K${FIRST}:$K${LAST}", f"$U${FIRST}:$U${LAST}")
for k, comp in enumerate(COMPS):
    rr = FIRST + k
    ws.cell(rr, B0, comp).font = f_txt
    ws.cell(rr, B0 + 1, f'=_xlfn.MINIFS({P},{I_},Z{rr},{J},"<>Aire libre")')
    ws.cell(rr, B0 + 2, f'=_xlfn.MINIFS({P},{I_},Z{rr},{J},"<>Sótano")')
    ws.cell(rr, B0 + 3, f'=SUMIFS({P},{I_},Z{rr},{J},"<>Aire libre",{T},"Elegido")+SUMIFS({P},{I_},Z{rr},{J},"<>Aire libre",{T},"Comprado")')
    ws.cell(rr, B0 + 4, f'=SUMIFS({P},{I_},Z{rr},{J},"<>Sótano",{T},"Elegido")+SUMIFS({P},{I_},Z{rr},{J},"<>Sótano",{T},"Comprado")')
    ws.cell(rr, B0 + 5, REF[comp]).font = f_txt
    for i in range(6):
        c = ws.cell(rr, B0 + i); c.border = box
        if 1 <= i <= 4: c.font = f_calc; c.fill = fill_calc; c.number_format = COP
tr = FIRST + len(COMPS)
ws.cell(tr, B0, "Total").font = f_lbl
for i in range(1, 5):
    L = ws.cell(tr, B0 + i).column_letter
    c = ws.cell(tr, B0 + i, f"=SUM({L}{FIRST}:{L}{tr-1})"); c.font = Font(name=F, size=10, bold=True); c.number_format = COP; c.fill = fill_calc; c.border = box
ws.cell(tr + 1, B0, "Las referencias son rangos estimados del informe de montaje, no cotizaciones.").font = Font(name=F, size=9, italic=True, color="5B6B82")

# ---------- Resumen ----------
R = resumen
R.sheet_view.showGridLines = False
R["A1"] = "MinuteMark · Presupuesto del punto"; R["A1"].font = f_title
R["A2"] = "Se llena solo con lo que se escriba en cada hoja. Si un ítem no tiene opción elegida, se presupuesta con la más barata."; R["A2"].font = f_txt
rh = ["Ítem", "Cantidad", "Proveedores registrados", "Con precio", "Más barata (COP)", "Más cara (COP)", "Elegida (COP)", "Para presupuesto (COP)", "Elegidos"]
for i, h in enumerate(rh, 1):
    c = R.cell(4, i, h); c.font = f_hdr; c.fill = fill_hdr; c.alignment = Alignment(wrap_text=True, vertical="center"); c.border = box
R.row_dimensions[4].height = 32
widths = [30, 10, 13, 10, 16, 16, 16, 18, 10]
for i, w in enumerate(widths, 1): R.column_dimensions[R.cell(4, i).column_letter].width = w
r = 5
def rng(sh, L): return f"'{sh}'!${L}${FIRST}:${L}${LAST}"
for ws_, label in sheets:
    sh = ws_.title
    R.cell(r, 1, label).font = f_txt
    R.cell(r, 2, f"='{sh}'!B3").font = f_link
    R.cell(r, 3, f"=COUNTA({rng(sh,'B')})")
    R.cell(r, 4, f"=COUNT({rng(sh,'Q')})")
    R.cell(r, 5, f'=IF(D{r}=0,"",MIN({rng(sh,"Q")}))')
    R.cell(r, 6, f'=IF(D{r}=0,"",MAX({rng(sh,"Q")}))')
    R.cell(r, 7, f'=IF(I{r}=0,"",SUMIFS({rng(sh,"Q")},{rng(sh,"U")},"Elegido")+SUMIFS({rng(sh,"Q")},{rng(sh,"U")},"Comprado"))')
    R.cell(r, 8, f'=IF(G{r}<>"",G{r},IF(E{r}="",0,E{r}))')
    R.cell(r, 9, f'=COUNTIF({rng(sh,"U")},"Elegido")+COUNTIF({rng(sh,"U")},"Comprado")')
    r += 1
last_item = r - 1
R.cell(r, 1, "Equipos y mobiliario").font = f_lbl
R.cell(r, 8, f"=SUM(H5:H{last_item})"); eq_row = r; r += 2
# estructura rows
R.cell(r, 1, "Estructura · parqueadero en sótano").font = f_txt
R.cell(r, 3, f"=COUNTA({rng('Estructura','B')})")
R.cell(r, 5, f"='Estructura'!AA{tr}"); R.cell(r, 7, f"=IF('Estructura'!AC{tr}=0,\"\",'Estructura'!AC{tr})")
R.cell(r, 8, f'=IF(G{r}<>"",G{r},E{r})'); s_row = r; r += 1
R.cell(r, 1, "Estructura · parqueadero al aire libre").font = f_txt
R.cell(r, 3, f"=COUNTA({rng('Estructura','B')})")
R.cell(r, 5, f"='Estructura'!AB{tr}"); R.cell(r, 7, f"=IF('Estructura'!AD{tr}=0,\"\",'Estructura'!AD{tr})")
R.cell(r, 8, f'=IF(G{r}<>"",G{r},E{r})'); a_row = r; r += 2
R.cell(r, 1, "Escenarios").font = Font(name=F, size=12, bold=True, color=AZUL); r += 1
scen = [("Punto en espacio ya cerrado", f"=H{eq_row}"), ("Punto en parqueadero de sótano", f"=H{eq_row}+H{s_row}"), ("Punto en parqueadero al aire libre", f"=H{eq_row}+H{a_row}")]
first_scen = r
for lab, fml in scen:
    R.cell(r, 1, lab).font = f_lbl; R.cell(r, 8, fml); r += 1
# styles
for rr in range(5, r):
    for cc in range(1, 10):
        c = R.cell(rr, cc)
        if c.value is None and rr not in (eq_row, s_row, a_row) and not (first_scen <= rr < r): continue
        if rr in (eq_row + 1, a_row + 1, first_scen - 1): continue
        c.border = box
        if cc >= 3 and c.value is not None and str(c.value).startswith("="):
            if c.font != f_link: c.font = f_calc
            c.fill = fill_calc
        if cc in (5, 6, 7, 8): c.number_format = COP
for rr in [eq_row] + list(range(first_scen, r)):
    R.cell(rr, 8).font = Font(name=F, size=11, bold=True)
R.cell(r + 1, 1, "Internet entra como costo del primer año (12 mensualidades + instalación).").font = Font(name=F, size=9, italic=True, color="5B6B82")
R.freeze_panes = "A5"

# ---------- Puntos (lo instalado en cada punto) ----------
PT = wb.create_sheet("Puntos")
PT.sheet_view.showGridLines = False
PT["A1"] = "Puntos montados: qué tiene cada uno y de dónde salió"; PT["A1"].font = f_title
PT["A2"] = "Una fila por equipo o mueble instalado. Si algo se daña en cualquier punto, aquí está el proveedor, el contacto y si la garantía sigue vigente."; PT["A2"].font = f_txt
PT["A3"] = "Se llena cuando se monta un punto. Las columnas grises se calculan solas."; PT["A3"].font = Font(name=F, size=9, italic=True, color="5B6B82")
ph = ["Punto", "Ubicación del punto", "Ítem", "Producto o referencia", "Cantidad", "Proveedor", "Contacto (nombre y WhatsApp)",
      "Fecha de compra o instalación", "Valor pagado (COP)", "Garantía (meses)", "Vence la garantía", "Estado de la garantía",
      "Serial o placa", "Factura (dónde está)", "Servicio técnico / mantenimiento", "Notas"]
pw = [24, 26, 14, 30, 9, 22, 24, 13, 15, 10, 13, 16, 16, 18, 26, 36]
PF, PL = 6, 105
for i, h in enumerate(ph, 1):
    c = PT.cell(HDR_ROW, i, h); c.font = f_hdr; c.fill = fill_hdr; c.alignment = Alignment(wrap_text=True, vertical="center"); c.border = box
    PT.column_dimensions[c.column_letter].width = pw[i - 1]
PT.row_dimensions[HDR_ROW].height = 42
for rr in range(PF, PL + 1):
    for i in range(1, len(ph) + 1):
        c = PT.cell(rr, i); c.border = box; c.alignment = wrap; c.font = f_in
    PT.cell(rr, 8).number_format = "dd/mm/yyyy"; PT.cell(rr, 9).number_format = COP
    k = PT.cell(rr, 11, f'=IF(OR(H{rr}="",J{rr}=""),"",EDATE(H{rr},J{rr}))'); k.number_format = "dd/mm/yyyy"
    l = PT.cell(rr, 12, f'=IF(K{rr}="","",IF(K{rr}<TODAY(),"Vencida",IF(K{rr}-TODAY()<=30,"Vence en "&(K{rr}-TODAY())&" días","Vigente")))')
    for c in (k, l): c.font = f_calc; c.fill = fill_calc
ITEMS = ["Nevera", "Congelador", "Estantería", "Repisa", "Torre", "Mesón", "Cámara", "Datáfono", "Internet", "LED y gráfica", "Estructura", "Otro"]
dv = DataValidation(type="list", formula1='"' + ",".join(ITEMS) + '"', allow_blank=True); PT.add_data_validation(dv); dv.add(f"C{PF}:C{PL}")
PT.freeze_panes = "B6"
PT.auto_filter.ref = f"A{HDR_ROW}:P{PL}"

# ---------- Fotos ----------
FS = wb.create_sheet("Fotos")
FS.sheet_view.showGridLines = False
FS["A1"] = "Fotos de las opciones"; FS["A1"].font = f_title
FS["A2"] = "Un bloque por opción. El número es el # de la fila en la hoja del ítem."; FS["A2"].font = f_txt
FS.column_dimensions["A"].width = 34
for col in "BCDEF": FS.column_dimensions[col].width = 24
gal = [("Neveras · opción 1", "2 puertas, 1,00 × 2,00 m, desde $4.000.000", ["nevera-frozentech-2p-a.webp", "nevera-frozentech-2p-b.webp", "nevera-frozentech-2p-c.png"]),
       ("Neveras · opciones 2 a 4", "1 puerta, 1,50 / 1,80 / 2,00 m, de $1.300.000 a $1.900.000 (fotos de referencia)", ["nevera-frozentech-1p-a.webp", "nevera-frozentech-1p-b.webp"])]
r = 4
for title, sub, files in gal:
    FS.cell(r, 1, title).font = f_lbl
    FS.cell(r + 1, 1, sub).font = f_txt; FS.cell(r + 1, 1).alignment = wrap
    FS.row_dimensions[r + 1].height = 240
    for i, fn in enumerate(files):
        out, _ = thumb(fn)
        xi = XLImage(out); scale = 300 / xi.height; xi.height = 300; xi.width = int(xi.width * scale)
        FS.add_image(xi, f"{chr(66 + i)}{r + 1}")
    r += 3

wb.save(OUT)
print("ok", eq_row, s_row, a_row, tr)
