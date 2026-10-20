# Oficina MinuteMark

Herramienta interna de los socios. No es parte de la landing: vive en esta carpeta, no usa ni cambia ningún archivo de la landing, y GitHub Pages no la publica (Pages deja por fuera las carpetas que empiezan con `_`).

## Dónde se usa

La oficina compartida está en claude.ai:

https://claude.ai/artifact/7JRogiZ5KaNFzfb7QSRP59

Ahí todo lo que se anota queda guardado en una base de datos compartida y se actualiza en vivo para los dos socios.

**Para que los dos puedan editar:** con el acceso «Cualquiera con el enlace», quien no es de la organización de Simón en Claude solo puede mirar. Simón entra a **Compartir**, invita a Sebastián con su correo como **Editor** y apaga el acceso con enlace. Sebastián la abre con su cuenta de claude.ai de ese correo, desde la app de Claude o desde Chrome o Safari (no desde el navegador de WhatsApp). Si una vista no puede guardar, la oficina lo dice con un aviso rojo arriba.

Si abren este `index.html` directo desde el repositorio, funciona como copia local: guarda solo en ese navegador y no ve lo de la oficina compartida.

## Salas

| Sala | Para qué |
| --- | --- |
| Inicio | Al llegar: saludo, foco del día, cuenta regresiva a la reunión, lo pendiente de hoy, el norte y las metas, los recordatorios, las tareas por área, lo último que pasó y el parqueadero. |
| Tablero | Todas las tareas en Por hacer · En curso · Hecho, con las áreas arriba para filtrar. Cada tarea con área, responsable, día, pasos, sus avances y, al cumplirla, cómo se cumplió. |
| Semana | Un foco por día y las tareas de cada día. Las tareas sin día quedan abajo para programarlas. |
| Reunión de las 6 | La reunión diaria en cuatro bloques: lo cumplido, lo avanzado y lo atrasado (10 min), el foco y las tareas de hoy (30), decisiones (10) y compromisos para mañana (10). Guarda notas, decisiones y actas. |
| Finanzas y proveedores | Las tareas abiertas del área Financiero y legal; la ficha de cada proveedor (cómo se pide, entrega, cuánto dura el producto, pedido mínimo, si cambian lo que se vence, lista 2026 e IVA) con sus pedidos; las cotizaciones de estanterías y la lista de precios con el margen de cada producto. |
| Comercial | Las tareas abiertas del área Comercial y las unidades y empresas de administración por etapa: por contactar → contactado → reunión → presentación → consejo → firmado. Cada contacto queda registrado con su próximo paso. |
| Libreta | Notas compartidas que se guardan solas: modelo de negocio, objeciones, guion de llamada, preguntas para financieros y proveedores. |
| Caja fuerte | NIT, bancos, códigos y accesos de proveedores, contraseñas y contactos, cifrados con una clave que solo tienen los dos socios. |
| Historial | La papelera (lo borrado se guarda 30 días y se puede restaurar), los cambios del día que se pueden deshacer y todos los movimientos. |

## Áreas

Cada tarea va en un área: **Comercial**, **Financiero y legal**, **Operación** o **Publicidad y redes**. Las áreas se crean, se renombran y se ordenan desde el Tablero. Las tareas comerciales también salen en la sala Comercial y las financieras en Finanzas y proveedores, así no hay que buscarlas en dos partes.

## Caja fuerte

- Todo lo que se guarda se cifra en el navegador (AES-GCM de 256 bits, con la llave sacada de la clave con PBKDF2-SHA-256 y 310.000 vueltas). En la base de datos solo queda texto cifrado: sin la clave nadie lo lee, tampoco Claude.
- La clave la eligen los dos al crear la caja (mínimo 10 caracteres) y se puede cambiar desde la misma sala. **Si se olvida, lo guardado no se recupera.**
- Se cierra sola al salir de la sala o tras 10 minutos sin uso. Lo de la caja no sale en el buscador ni en el historial de cambios.
- Solo la pueden leer el dueño y quienes tienen permiso de Editor (regla de la base de datos sobre `caja`); con el enlace público no se ve ni el texto cifrado.
- Si Claude carga datos, quedan en `caja/semilla` y entran cifrados la próxima vez que un socio abre la caja; ahí mismo se borra la semilla.
- Las claves no se escriben en ninguna otra parte de la oficina ni se le mandan a Claude por chat.

## Pedidos a proveedores

En cada ficha, «Registrar pedido» anota qué se pidió, cuándo llega y cuánto costó. El pedido queda «en camino» (en rojo si ya debía haber llegado) hasta que se marca «Ya llegó»; ahí la oficina recuerda anotar la fecha de vencimiento. Los pedidos quedan en la ficha y salen en el buscador.

## Lo que se empieza y no se termina

Con **Registrar avance** se anota qué se hizo, qué falta, qué día se sigue y quién sigue. La tarea queda en curso para ese día, con el último avance a la vista, y la reunión siguiente la muestra en «Avanzado, sin terminar». Se cierra solo cuando se marca como hecha y se cuenta cómo se cumplió.

## Fechas límite, recordatorios y correos

- **Día** es cuándo se trabaja una tarea; **fecha límite** es cuándo tiene que estar lista. Con fecha límite, la tarea muestra «Vence en N días», «Vence mañana», «Vence hoy» o «Venció hace N días», y la oficina avisa en pantalla cuando faltan 1 día o menos.
- Los **recordatorios** tienen día, hora opcional y para quién son (Simón, Sebastián o ambos). Con la oficina abierta salen en pantalla a su hora.
- **Correos diarios** a cada socio, con lo suyo y lo de los dos: 6:56 a.m. y 5:20 p.m. (hora de Medellín). Los envía Claude desde la conversación de la oficina, con el Gmail de Simón.
- **Cómo insisten las fechas límite:** desde el día de aviso (7 días antes por defecto; puede ser 3, 14 o 30) la tarea sale en «Plazos que se acercan» del correo de la mañana. A 3 días o menos pasa a «Urgente», arriba de los dos correos del día. El día que vence, el asunto dice «Vence hoy». Si se vence, sigue saliendo como «Venció hace N días» hasta que se marque como hecha. Los recordatorios vencidos también se repiten cada mañana hasta marcarlos.
- **Google Calendar (lo más confiable):** cada recordatorio y cada fecha límite tiene el botón «Agregar al calendario». Abre Google Calendar con la fecha, la hora y el otro socio invitado; se guarda y listo. Desde ahí los avisos al celular y al correo los manda Google, aunque nadie abra la oficina ni Claude. Los correos de los socios están en Ajustes (el lápiz del Norte).
- **Control:** cada envío deja la hora en la oficina («Último envío»). Si pasan más de 15 horas sin correo, la oficina muestra un aviso en rojo.

## Nada se pierde y todo se edita

- **Deshacer:** después de cada cambio sale un aviso con el botón «Deshacer». También está en la barra lateral y con Ctrl + Z (Cmd + Z en Mac). Los cambios del día se pueden deshacer uno a uno, del más reciente al más viejo.
- **Papelera:** lo que se borra (tareas, notas, decisiones, ideas, recordatorios, proveedores, cotizaciones, productos, prospectos, metas, áreas, focos) queda 30 días en Historial › Papelera para restaurarlo.
- **Todo se edita:** tareas, avances, decisiones, ideas del parqueadero (también las descartadas), recordatorios (también los hechos), el historial de contactos de cada prospecto y las áreas con su orden.
- **Buscar:** el botón Buscar (o Ctrl + K) encuentra cualquier cosa de la oficina y la abre.
- **Volver:** arriba de cada sala hay un botón para volver a la sala anterior; «Inicio» siempre lleva a la entrada.
- **Copia de seguridad:** en Historial se descarga una copia completa (.json) o las tareas en Excel (.csv). La información vive en la oficina de claude.ai, no en la conversación con Claude.
- **Vista tranquila:** cada panel se oculta o se muestra con la flecha de su esquina, y cada socio ve la oficina como la dejó. En la Reunión de las 6, «Modo pantalla» oculta la barra lateral, agranda todo y, con la reunión en curso, deja abierto solo el bloque del momento.

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
