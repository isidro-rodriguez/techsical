# Registro de cambios

Formato de [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y versiones
[SemVer](https://semver.org/lang/es/).

## [Sin publicar]

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
