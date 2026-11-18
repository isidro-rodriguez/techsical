/*
 * techsical: la imagen de un enlace «vuela» hasta la imagen principal de la
 * página de destino (portada, tarjeta o listado → artículo).
 *
 * Al salir (pageswap) se busca un enlace a la página de destino que contenga una
 * imagen; si lo hay, se le da un nombre de transición y se anota el destino. Al
 * llegar (pagereveal) se da el mismo nombre a la primera imagen del artículo, y
 * el navegador anima una hacia la otra. Se carga en <head> sin defer porque
 * pagereveal llega antes del primer pintado.
 */
(() => {
  const NAME = "tx-image";
  const KEY = "techsical:transition-image";

  const samePage = (a, b) => new URL(a, location.href).pathname === new URL(b).pathname;

  window.addEventListener("pageswap", (event) => {
    const entry = event.activation && event.activation.entry;
    if (!event.viewTransition || !entry) return;
    for (const link of document.querySelectorAll("a[href]")) {
      const image = link.querySelector("img");
      if (image && samePage(link.href, entry.url)) {
        image.style.viewTransitionName = NAME;
        try {
          sessionStorage.setItem(KEY, new URL(entry.url).pathname);
        } catch {
          /* Sin sessionStorage no hay imagen compartida: la página se funde igual. */
        }
        return;
      }
    }
  });

  window.addEventListener("pagereveal", (event) => {
    let target = null;
    try {
      target = sessionStorage.getItem(KEY);
      sessionStorage.removeItem(KEY);
    } catch {
      return;
    }
    if (!event.viewTransition || target !== location.pathname) return;
    const tag = () => {
      const image = document.querySelector(".md-content article img, .md-content__inner img");
      if (image) image.style.viewTransitionName = NAME;
    };
    // pagereveal puede llegar antes de que el cuerpo esté analizado.
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", tag, { once: true });
    } else {
      tag();
    }
  });
})();
