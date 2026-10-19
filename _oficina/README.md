# Oficina MinuteMark

Herramienta interna de los socios. No es parte de la landing: vive en esta carpeta, no usa ni cambia ningún archivo de la landing, y GitHub Pages no la publica (Pages deja por fuera las carpetas que empiezan con `_`).

## Dónde se usa

La oficina compartida está en claude.ai:

https://claude.ai/artifact/7JRogiZ5KaNFzfb7QSRP59

Ahí todo lo que se anota queda guardado en una base de datos compartida y se actualiza en vivo para los dos socios. Para que Sebastián entre, Simón la comparte desde el menú **Compartir** de la página (Sebastián tiene que estar en la misma organización de Claude).

Si abren este `index.html` directo desde el repositorio, funciona como copia local: guarda solo en ese navegador y no ve lo de la oficina compartida.

## Salas

| Sala | Para qué |
| --- | --- |
| Recepción | Al llegar: saludo, foco del día, cuenta regresiva a la reunión, lo pendiente de hoy, el norte y las metas, los recordatorios, la ruta, lo último que pasó y el parqueadero. |
| Tablero | La ruta a la primera venta (5 etapas) y todas las tareas en Por hacer · En curso · Hecho. Cada tarea con responsable, día, pasos, sus avances y, al cumplirla, cómo se cumplió. |
| Semana | Un foco por día y las tareas de cada día. Las tareas sin día quedan abajo para programarlas. |
| Reunión de las 6 | La reunión diaria en cuatro bloques: lo cumplido (10 min), foco de hoy (30), decisiones (10) y compromisos para mañana (10). Guarda notas, decisiones y actas. |
| Proveedores y precios | Lista de precios 2026 e IVA por proveedor, cotizaciones de estanterías comparadas contra el proveedor actual y la lista de precios con el margen de cada producto. |
| Comercial | Unidades y empresas de administración por etapa: por contactar → contactado → reunión → presentación → consejo → firmado. Cada contacto queda registrado con su próximo paso. |
| Libreta | Notas compartidas que se guardan solas: modelo de negocio, objeciones, guion de llamada, preguntas para financieros y proveedores. |

## Lo que se empieza y no se termina

Con **Registrar avance** se anota qué se hizo, qué falta, qué día se sigue y quién sigue. La tarea queda en curso para ese día, con el último avance a la vista, y la reunión siguiente la muestra en «Avanzado, sin terminar». Se cierra solo cuando se marca como hecha y se cuenta cómo se cumplió.

## Fechas límite, recordatorios y correos

- **Día** es cuándo se trabaja una tarea; **fecha límite** es cuándo tiene que estar lista. Con fecha límite, la tarea muestra «Vence en N días», «Vence mañana», «Vence hoy» o «Venció hace N días», y la oficina avisa en pantalla cuando faltan 1 día o menos.
- Los **recordatorios** tienen día, hora opcional y para quién son (Simón, Sebastián o ambos). Con la oficina abierta salen en pantalla a su hora.
- **Correos diarios** a cada socio, con lo suyo y lo de los dos: 6:56 a.m. y 5:20 p.m. (hora de Medellín). Los envía Claude desde la conversación de la oficina, con el Gmail de Simón.
- **Cómo insisten las fechas límite:** desde el día de aviso (7 días antes por defecto; puede ser 3, 14 o 30) la tarea sale en «Plazos que se acercan» del correo de la mañana. A 3 días o menos pasa a «Urgente», arriba de los dos correos del día. El día que vence, el asunto dice «Vence hoy». Si se vence, sigue saliendo como «Venció hace N días» hasta que se marque como hecha. Los recordatorios vencidos también se repiten cada mañana hasta marcarlos.
- **Control:** cada envío deja la hora en la oficina («Último envío»). Si pasan más de 15 horas sin correo, la oficina muestra un aviso en rojo.

## Reglas de la oficina

1. Un foco por día. Lo que no es del foco va al parqueadero.
2. Nada sale de la reunión sin responsable y día.
3. Lo cumplido se causa: una línea sobre cómo se cumplió, con datos.
4. Lo decidido no se reabre sin un dato nuevo.

## Archivos

```
index.html   La oficina completa (HTML, CSS y JavaScript, sin dependencias)
img/         Logo, isotipo y tres poses de Mark, tomados del Design System de MinuteMark
```

Para cambiar algo, se edita `index.html` y se vuelve a publicar en el mismo link desde Claude. Los datos no se pierden al publicar una versión nueva.
