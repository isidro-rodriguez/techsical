/*
 * techsical: fórmulas LaTeX con MathJax ([project.extra.techsical] math = true).
 *
 * Requiere la extensión pymdownx.arithmatex con generic = true, que envuelve las
 * fórmulas en .arithmatex con \( \) y \[ \]. Este archivo se carga (defer) antes
 * que MathJax: define su configuración y, como Zensical cambia de página sin
 * recargar (navigation.instant), vuelve a componer las fórmulas en cada página.
 */
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex",
  },
};

if (typeof document$ !== "undefined") {
  document$.subscribe(() => {
    // En la primera página MathJax aún no ha arrancado: compone él solo al cargar.
    if (!window.MathJax.startup || !window.MathJax.startup.output) return;
    MathJax.startup.output.clearCache();
    MathJax.typesetClear();
    MathJax.texReset();
    MathJax.typesetPromise();
  });
}
