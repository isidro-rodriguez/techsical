# Registro de cambios

Formato de [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y versiones
[SemVer](https://semver.org/lang/es/).

## [Sin publicar]

## [0.4.0] - 2026-11-18

### Añadido

- Portada: con imágenes en el hero, el texto anterior al primer `##` (la
  introducción) va en la columna del hero, al lado de las imágenes. Bajo el
  hero, el texto corrido mantiene la medida del artículo (`content_max`);
  tablas y tarjetas siguen a todo el ancho.

### Corregido

- Las páginas sin índice lateral porque la web sobrescribe el bloque
  `site_nav` (reCocina) no centraban el artículo.
- Las etiquetas (`md-tag`) se subrayaban como enlaces y su icono apenas se veía.

- Con `framed`, el título fijo del índice lateral tenía el fondo del panel en
  vez del de la página.
- El código de la primera columna de las tablas se partía a mitad de palabra
  (`atril.tom` / `l`) cuando la columna era estrecha.

## [0.3.0] - 2026-11-18

### Añadido

- Estilo para la referencia de la API de mkdocstrings: nombres en
  monoespaciada, objetos separados por líneas, etiquetas y títulos de sección
  como rótulos y símbolos con los colores del tema. La demostración incluye la
  API de un paquete de ejemplo y una guía para configurarla.

### Corregido

- «Anterior / siguiente» al pie seguía visible con `footer_nav` desactivado:
  la regla de Zensical era más específica.

## [0.2.0] - 2026-11-18

### Añadido

- Opciones de maquetación en `[project.extra.techsical]`: `toc = false` quita el
  índice lateral de todas las páginas y centra el artículo; `framed = true` pone
  el artículo en un panel sobre un fondo de página más oscuro, con las migas de
  pan separadas del panel; `footer_nav = true`
  muestra «anterior / siguiente» al pie.
- Transiciones suaves entre páginas (View Transitions entre documentos), con la
  imagen de un enlace que se desplaza hasta la de la página de destino;
  `transitions = false` las quita.
- Sin `primary_dark` ni `accent_dark`, el modo oscuro los deriva de los colores
  claros de la web.

### Cambiado

- `navigation.instant` deja de estar entre las features por defecto: anula las
  transiciones entre páginas.
- La primera imagen de la portada se carga con prioridad en lugar de diferirse.
- «Anterior / siguiente» al pie queda oculto por defecto y nunca aparece en la
  portada.

### Corregido

- En pantallas estrechas, el artículo sin índice lateral conserva los márgenes
  de Zensical en lugar de pegarse a los bordes.

## [0.1.0] - 2026-11-18

### Añadido

- Tema `techsical` que extiende el de Zensical (`zensical>=0.1.2,<0.2`).
- Colores en capas (primitivas, marca, semánticas por esquema) con tema claro y
  oscuro propios; contraste WCAG AA comprobado en los tests.
- Fuentes propias, sin Google Fonts: Source Serif 4 (texto y títulos), Manrope
  (interfaz, tablas y pies) y JetBrains Mono (código).
- Cabecera editorial con la marca (nombre y descripción) y, debajo, una barra de
  navegación propia opcional (`header_nav`).
- Portada `home.html` con entradilla, botones y hasta dos imágenes.
- Artículos con entradilla (`{ .lead }`), índice lateral opcional, imágenes
  centradas sin ampliar, tablas a todo el ancho y notas planas por estado.
- Personalización en `[project.extra.techsical]`: colores, fuentes, anchos,
  favicons, manifiesto y color del navegador.
- Estilo propio para listas de definiciones, pestañas y listas de tareas.
- Fórmulas LaTeX con MathJax (`math = true`) y diagramas Mermaid con los colores
  del tema.
