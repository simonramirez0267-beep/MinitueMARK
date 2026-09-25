# MinuteMark · Landing

Landing de una sola página para MinuteMark, el mercado honesto y autónomo que vive dentro de las unidades residenciales de Medellín.

Es un sitio estático: HTML, CSS y JavaScript sin dependencias ni proceso de compilación. Cualquier hosting de archivos lo sirve tal cual.

## Estructura

```
index.html              La página
favicon.png             Ícono de la pestaña
og-image.png            Imagen que se ve al compartir el link (WhatsApp, redes)
robots.txt
assets/
  css/styles.css        Todos los estilos
  js/main.js            Formularios, botón flotante y animaciones al hacer scroll
  fonts/                Outfit (tipografía de la marca), alojada en el sitio
  img/
    fotos/              Fotos de residentes (key visual del manual)
    marca/              Logo e isotipo de MinuteMark
    mark/               Mark, el personaje (tres poses)
    aliados/            Logos de distribuidores, marcas del surtido, SANAR y pilas
```

## Verlo en el computador

Abre `index.html` con doble clic. Para verlo exactamente como en internet, sírvelo desde la carpeta:

```
python3 -m http.server 8000
```

y entra a `http://localhost:8000`.

## Publicarlo

- **GitHub Pages:** en el repositorio, Settings → Pages → Deploy from a branch → `main` y carpeta `/ (root)`.
- **Netlify o Vercel:** importa el repositorio. No hay comando de build y la carpeta de publicación es la raíz.

Cuando tengan dominio propio:

1. Cambia `og-image.png` por la dirección completa (`https://tudominio.com/og-image.png`) en las etiquetas `og:image` y `twitter:image` de `index.html`. Así el link se ve con imagen al compartirlo por WhatsApp.
2. Agrega `<link rel="canonical" href="https://tudominio.com/">` en el `<head>`.

## Formularios → WhatsApp

Los dos formularios ("¿Aplica tu unidad?" y "Hablemos") hoy solo muestran el mensaje de gracias: **los datos no llegan a ninguna parte**.

Para recibirlos, escribe el número comercial en la primera línea de `assets/js/main.js`:

```js
var MM_WHATSAPP = '573001234567'; // solo dígitos, con el 57
```

Con el número puesto, al enviar se abre WhatsApp con los datos ya escritos y la persona solo toca enviar.

## Reglas de marca

Colores, tipografía, uso de Mark y emblemas salen del Design System de MinuteMark. Antes de cambiar un color, un tamaño o una pose de Mark, revísalo allá. Lo más importante:

- Una sola tipografía: Outfit.
- Mark va solo sobre azul (degradado, azul profundo o tinta), una pose por sección.
- Los acentos verde y violeta, y el azul de Mark en 24/7, viven solo dentro de los emblemas de "Qué es MinuteMark".
- En texto, la marca se escribe MinuteMark: una palabra, dos M mayúsculas.

## Créditos

- Tipografía Outfit bajo la SIL Open Font License 1.1 (`assets/fonts/OFL.txt`).
- Los logos de distribuidores y marcas son propiedad de sus dueños y se muestran como referencia del surtido.
- Mark es el personaje de MinuteMark, diseñado por R&S Creative Studio.
