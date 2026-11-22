# Cotizaciones del punto físico

Aquí está el banco de cotizaciones para montar los puntos de MinuteMark: todas las opciones de cada cosa que necesita un punto, con foto, precio y condiciones. También guarda qué quedó instalado en cada punto. Sirve de plan B cuando un proveedor o un comodato se cae, y de memoria para montar el punto 2, 3 y los que siguen.

## El archivo

**Versión viva, la que se edita:** [MinuteMark · Cotizaciones del punto](https://docs.google.com/spreadsheets/d/1P48TY4e64aG82Fdq-Y9YP509qPtEpTX2Zn1f2hIgOXg/edit), en el Drive compartido de MinuteMark › 04 Finanzas y precios › Montaje del punto (subida el 22 nov 2026). Simón y Sebastián la editan ahí.

`MinuteMark-Cotizaciones-Punto.xlsx` (en esta carpeta) es la copia de respaldo con la que se armó, y la base para pasar todo a la Oficina.

| Hoja | Para qué |
| --- | --- |
| Resumen | Por ítem: cuántas opciones hay, la más barata, la más cara y la elegida. Abajo, el total del punto en tres escenarios: espacio cerrado, parqueadero en sótano y parqueadero al aire libre. |
| Cómo usar | Qué celdas se llenan, el IVA y un ejemplo de fila. |
| Neveras, Congeladores, Estanterías, Repisas y torre, Mesón de pago, Cámaras, Pagos y datáfono, Internet, Luz y gráfica | Una fila por opción. La foto va en la columna C, al lado del proveedor. |
| Estructura | Lo que hay que construir si el punto va en un parqueadero: una fila por componente (muros, techo, piso, fachada, eléctrico, ventilación…), marcando si aplica a sótano, aire libre o ambos. |
| Puntos | Lo que quedó instalado en cada punto: proveedor, contacto, fecha, valor, garantía, serial, factura y servicio técnico. Calcula cuándo vence la garantía y avisa. |
| Fotos | Las fotos adicionales de cada opción. |

Otras carpetas:

- `fotos/`: todas las fotos de las opciones (pantallazos de proveedores y fotos de las tiendas), con nombre por ítem y proveedor.
- `herramientas/exportar_a_oficina.py`: pasa el Excel (datos y fotos) a `montaje-oficina.json`, el archivo que carga la sala Montaje de la Oficina.
- `herramientas/construir_excel.py`: arma el Excel desde cero con los datos y las fotos. Se corre con `python3 cotizaciones/herramientas/construir_excel.py cotizaciones/MinuteMark-Cotizaciones-Punto.xlsx`. Cuando se agrega una cotización, se agrega en este archivo y se vuelve a armar el Excel, así el Excel nunca queda desordenado.

Reglas que no se cambian sin decidirlo:

- **Módulo de estantería universal:** 1,80 m de alto (mínimo) × 63 cm de ancho × 30 cm de fondo, entrepaños graduables, madera o melamina (nada industrial). Se acepta ancho 60–66, fondo 28–32 y alto 180–185 cm; lo demás no entra.
- Los precios se comparan siempre con IVA: si un proveedor cotiza sin IVA, el Excel se lo suma.
- Una opción pasa a «Elegido» o «Comprado» y el Resumen la toma; si no hay ninguna elegida, presupuesta con la más barata.

## Plan: pasarlo a la Oficina

**Estado (22 nov 2026):** la sala «Montaje» está construida en la rama `claude/exciting-keller-rbo96a`, esperando el visto bueno de Simón para pasar a `main`. Para cargar el Excel: `python3 cotizaciones/herramientas/exportar_a_oficina.py` arma `montaje-oficina.json` y en la Oficina › Montaje se toca «Cargar las cotizaciones del Excel». Una vez cargado, las cotizaciones nuevas se escriben en la Oficina, no en el Excel.

Cuando estén cerradas las primeras cotizaciones (internet, estanterías, neveras y congeladores), esto pasa a la Oficina con estas condiciones, acordadas con Simón el 21 de noviembre de 2026:

1. **Una sala nueva y aparte**, al estilo de la Caja fuerte: su propia entrada en la barra lateral y nada más. **No se cambia ninguna otra sala, ni el Inicio, ni el orden de lo que ya existe.** La pestaña «Estanterías» de Finanzas y proveedores se queda como está.
2. **Mismo orden que el Excel:** una pestaña por ítem, el mismo resumen y los mismos tres escenarios. Cada opción se ve como tarjeta con la foto grande, precio, proveedor, garantía, entrega, forma de pago y estado.
3. **Fotos:** se suben desde el celular (pantallazos de Marketplace o WhatsApp) y se guardan comprimidas con la cotización. La política de seguridad de la Oficina ya admite imágenes `data:`.
4. **Entrada inicial:** un botón para importar este Excel, de modo que nada se escribe dos veces.
5. **Puntos (se activa después del primer montaje):** cada punto con su ficha de lo instalado, igual que la hoja Puntos. Desde la ficha de un equipo se llega al proveedor y a su contacto, y la Oficina avisa cuando una garantía está por vencer.
6. **Crece con el proyecto:** las pestañas de ítems se pueden agregar, renombrar y ordenar, porque van a salir proveedores y necesidades nuevas.
7. Se construye en una rama, se muestra antes y solo pasa a `main` cuando Simón lo apruebe.
