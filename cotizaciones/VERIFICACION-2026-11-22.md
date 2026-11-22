# Verificación de las cotizaciones · 22 nov 2026

Pedida por Simón: confirmar que ningún precio, foto o dato quedó cruzado al pasar las cotizaciones entre sesiones de Claude, el Excel, el Drive y la Oficina. Hecha por Claude con programas que comparan dato por dato, no a ojo.

## 1. La cadena de copias: sin errores de datos

| Comparación | Qué se revisó | Resultado |
| --- | --- | --- |
| Datos originales (`herramientas/construir_excel.py`) → Excel del repositorio | Se volvió a armar el Excel y se comparó con el guardado: todas las hojas, todas las celdas y la posición de cada foto | 15.681 celdas, 0 diferencias |
| Excel del repositorio → hoja viva del Drive | Se descargó la hoja del Drive y se comparó celda por celda | 2.278 celdas con dato, 0 diferencias de contenido (Google solo escribe las fórmulas sin comillas) |
| Excel → archivo que carga la Oficina (`montaje-oficina.json`) | Los 21 campos de las 38 opciones (798 datos), la cantidad y la necesidad de cada ítem | 0 diferencias |
| Fotos de cada opción | Que cada opción tenga la foto de su fila y las de la hoja Fotos | 1 error, corregido (ver abajo) |
| Lo que muestra la Oficina → lo que calcula Google | Proveedor, costo total y número de fotos de las 38 tarjetas | 38 de 38 iguales |
| Precio contra sus propias notas | Los valores en pesos que menciona cada nota (combos, precios normales) | Todos cuadran: combo de 2 a $689.900 = $344.950 c/u; combo de 3 a $1.099.900 = $366.633 c/u; paquete de 2 cámaras a $239.900 = $119.950 c/u |
| Historial de versiones del Excel (8 versiones en GitHub) | Cada cambio de precio entre versiones | 6 cambios, todos el 22 nov con la página a la vista. Uno corrigió un cruce: la estantería menta 718067 tenía $619.900 (el precio de la negra 688708) y quedó en $297.900. Hoy la página confirma los dos precios. |

Totales del punto, iguales en el Drive y en la Oficina: equipos y mobiliario **$4.605.700**; espacio cerrado, sótano y aire libre **$4.605.700** (Estructura todavía no tiene cotizaciones).

**Error encontrado y corregido:** al pasar el Excel a la Oficina, las 4 neveras quedaron con una sola foto: faltaban las de la hoja Fotos (3 de la nevera de 2 puertas, 2 de las de 1 puerta). Los precios no estaban afectados. Se corrigió `herramientas/exportar_a_oficina.py` y se volvió a armar `montaje-oficina.json`.

## 2. Precios contra las páginas, hoy 22 nov 2026

Esto ya no es la copia: es si el precio del mercado sigue igual. Los precios cambian; cada uno vale con su fecha.

| Opción | En las cotizaciones | En la página hoy | Qué hacer |
| --- | --- | --- | --- |
| Estantería Home E3, 656368 (y Mesón opción A) | $249.900 | $249.900, **promoción hasta el 23 nov**; precio normal $479.900 | Si se va a comprar, comprar ya o presupuestar con $479.900 |
| Combo Home 2 bibliotecas, 666936 | $344.950 c/u | $689.900 el combo (= $344.950 c/u) | Igual |
| Combo Home 3 bibliotecas, 661539 | $366.633 c/u | $1.099.900 el combo, **sin existencias** | Confirmar disponibilidad |
| Biblioteca Home macadamia (Falabella 140562805) | $359.900 | **Sin precio y sin existencias** | Marcar «Esperando respuesta» o descartar |
| Multy 360880 | $379.900 | $379.900 | Igual |
| Librero negro 688708 | $619.900 | $619.900, sin existencias | Igual |
| Librero menta 718067 | $297.900 | $297.900, sin existencias | Igual |
| Combo Home wengue 3 bibliotecas, 666923 | Sin precio | **$879.900 el combo (= $293.300 c/u)**, normal $1.349.900, hasta el 3 dic | Dato nuevo: se puede anotar; sería la estantería más barata de medida exacta |
| Colombia Move (usada) | $200.000 | **El anuncio expiró**; la página dice $150.000 | Descartar |
| Somos Internet (4 planes) | $63.000 / $100.000 / $75.000 / $120.000 | Iguales en los pantallazos guardados | Igual |
| Tapo C110 (Alkosto) | $99.900 | Alkosto no se pudo leer; en Falabella hay de $94.900 a $129.900 según el vendedor | Confirmar en la tienda |
| Tapo C110 paquete de 2 | $119.950 c/u | $239.900 el paquete | Igual |
| Tapo C210 | $89.900 | $89.900 en Falabella (vendedor Center System, no Homecenter); paquete de 2 a $181.900 | Corregir el proveedor a «Falabella (Center System)» |
| Tapo C220 | $154.900 | **Sin existencias** en Falabella | Confirmar |
| Ezviz H6c 2K | $120.900 | **No aparece**; solo la H6c G1 3K a $160.900 | Confirmar o descartar |
| Imou Ranger Mini, Tapo C225 | $139.899 / $197.910 | No se pudo leer la página | Confirmar |

No se pudieron revisar desde aquí: las neveras de Frozentech (Marketplace; ninguna foto guardada muestra el precio), las páginas del Éxito (bloquean la consulta) y Movistar, Claro y Starlink (la red de esta sesión no llega a esos sitios).

## 3. Recomendaciones

1. **Ningún precio se da por bueno para comprar sin confirmarlo ese día.** Antes de marcar «Elegido» o «Comprado», abrir el link o escribirle al proveedor y actualizar el precio y la fecha de cotización.
2. **Neveras:** guardar en la opción (botón Subir foto) el pantallazo del chat de Frozentech donde dan cada precio. Hoy $4.000.000, $1.300.000 y $1.900.000 no tienen prueba escrita.
3. La foto de la Imou está volteada en espejo (el logo se lee «uomi»); es la marca correcta.
