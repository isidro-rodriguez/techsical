# Fórmulas y diagramas

Fórmulas LaTeX con MathJax y diagramas de flujo Mermaid con los colores del tema.
{ .lead }

## Fórmulas

Con `math = true` en `[project.extra.techsical]` y la extensión
`pymdownx.arithmatex` (`generic = true`), las fórmulas se escriben en LaTeX. En
línea, como la tensión normal \(\sigma = N / A\) o el módulo
\(E_{cm} = 22\,(f_{cm}/10)^{0{,}3}\) GPa, y en bloque:

\[
M_{Ed} = \frac{q\,L^2}{8}
\qquad
\delta_{max} = \frac{5\,q\,L^4}{384\,E\,I}
\]

\[
f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(a)}{n!}\,(x-a)^n
\]

## Diagramas

Un solo hilo de pocos nodos, en horizontal y con líneas ortogonales:

``` mermaid
%%{init: {"flowchart": {"curve": "step"}}}%%
flowchart LR
  A[Lorem] --> B[Ipsum] --> C[Dolor] --> D[Sit amet]
```

Con ramas, en vertical:

``` mermaid
%%{init: {"flowchart": {"curve": "step"}}}%%
flowchart TD
  A[Lorem ipsum] --> B{¿Dolor sit?}
  B -- Sí --> C[Amet consectetur]
  B -- No --> D[Adipiscing elit]
  C --> E[Sed do eiusmod]
  E --> F{¿Tempor?}
  F -- Sí --> G[Incididunt ut labore]
  F -- No --> D
```
