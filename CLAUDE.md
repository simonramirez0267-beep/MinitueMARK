# MinuteMark · Cómo trabajar en este proyecto

MinuteMark es un minimercado autónomo y honesto que vive dentro de las unidades residenciales de Medellín. Socios: Simón Ramírez y Sebastián. Samuel es aliado estratégico (todavía no es socio) y está aprendiendo el negocio para salir a vender a edificios.

Desde noviembre de 2026 los socios trabajan a distancia: Simón está fuera de Medellín y Sebastián sigue allá, en prácticas. Por eso todo lo que se haga tiene que quedar claro y en su sitio, para que el otro pueda seguir sin preguntar.

## Reglas

1. **Todo queda causado.** Cada entrega se guarda donde corresponde (este repositorio, la Oficina o el Drive), con fecha, fuente y estado. Nada importante vive solo en la conversación.
2. **Cada cosa en un solo lugar.** Antes de crear algo nuevo, revisar si ya existe y ampliarlo.
3. **La Oficina no se reorganiza.** Lo nuevo entra como sala o pestaña nueva; no se mueve ni se cambia lo que ya existe sin que Simón lo apruebe. Se construye en una rama, se muestra y solo pasa a `main` con su visto bueno.
4. **Datos honestos.** Separar el dato público (con link o fuente) del estimado. Precios siempre comparados con IVA y con fecha de cotización.
5. **Cierre de cada trabajo:** qué se hizo, dónde quedó, qué falta y quién lo hace.
6. **Escribir para el que llega nuevo.** Que lo entienda Samuel sin contexto previo: español claro, sin jerga.
7. **Privacidad.** Este repositorio publica páginas en internet. Claves, bancos y datos sensibles van a la Caja fuerte de la Oficina, nunca aquí.
8. **Marca.** Colores, tipografía y uso de Mark según el README principal y el Design System.

## Mapa del repositorio

| Carpeta | Qué es |
| --- | --- |
| `/` | Landing de MinuteMark |
| `oficina/` | App interna de los socios (Firebase). Ver su README antes de tocarla |
| `modelo-3d/` | Modelo 3D del punto (Matriz 01, celda de parqueadero de 2,43 × 3,90 m) |
| `bosques/` | Propuesta para Bosques de la Cascada |
| `cotizaciones/` | Banco de cotizaciones del punto físico (Excel) y el plan para pasarlo a la Oficina |

## Decisiones vigentes del montaje

- **Módulo de estantería universal:** 1,80 m de alto (mínimo) × 63 cm de ancho × 30 cm de fondo, con entrepaños graduables. Madera o melamina, nada industrial. Es el formato «Home» de RTA Muebles.
- **Internet:** fibra óptica con respaldo 4G y UPS. Tigo quedó descartado. Somos Internet es la primera opción.
- **Neveras:** primer proveedor cotizado, Frozentech (Marketplace).
- **Oficina:** cuando se cierren las primeras cotizaciones se crea la sala «Montaje», con dos pestañas: Cotizaciones y Puntos. El plan completo está en `cotizaciones/README.md`.
