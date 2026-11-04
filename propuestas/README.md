# Propuestas comerciales · Maison Enterprises

Todas las propuestas para clientes y prospectos salen de **una sola plantilla**: la propuesta de Benelli Store (noviembre 2026). El diseño no se toca. Por cliente solo cambian los datos: nombre, contacto, textos, servicios y precios.

## Cómo está armado

```
propuestas/
├── build.py                      # genera el PDF
├── _plantilla/
│   ├── propuesta.html.j2         # el diseño (NO se edita por cliente)
│   └── fonts/                    # Inter + Newsreader (licencia OFL)
└── clientes/
    └── <cliente>/
        ├── datos.json            # lo único que se edita
        └── <Cliente>_Propuesta.pdf
```

## Nueva propuesta (paso a paso)

1. Copiar la carpeta del modelo: `clientes/benelli-store/` → `clientes/<nuevo-cliente>/`.
2. Editar `datos.json` del nuevo cliente:
   - `archivo`: nombre del PDF (sin `.pdf`), por ejemplo `IronBird_Propuesta`.
   - `titulo_pdf`: el título que se ve en el visor de PDF.
   - `cliente`: nombre del negocio, persona de contacto, dirección, @ de Instagram y nombre corto.
   - `fecha`: mes y año.
   - `portada`: el título (la segunda línea va en celeste) y las 4 tarjetas de servicios.
   - `paginas`: una entrada por página. Los textos y precios se cambian acá.
3. Generar el PDF:

```bash
python propuestas/build.py propuestas/clientes/<nuevo-cliente>/datos.json
```

Se necesita `jinja2` (`pip install jinja2`) y Chrome o Chromium. Si Chrome no aparece solo, se pasa la ruta con la variable `CHROME`.

## Qué se puede cambiar y qué no

- **Sí:** cualquier texto, cifra o precio; qué servicios se ofrecen; sacar o agregar páginas. El índice de la portada, los puntos del pie y la numeración `01 / 08` se ajustan solos.
- **No:** colores, tipografías, tamaños, márgenes ni la estructura visual. Todo eso vive en `_plantilla/propuesta.html.j2`.
- Si se saca un servicio, también hay que actualizar a mano:
  - las tarjetas de la portada,
  - el número del `kicker` de cada página (`01 · Publicidad en Meta`, `02 · Sitio web`…),
  - la página de Inversión.

## Piezas disponibles en `bloques`

| `tipo` | Qué dibuja | Campos |
|---|---|---|
| `kpis` | 4 tarjetas de datos (situación actual) | `items: [{label, valor}]` |
| `texto` | Sección numerada con párrafos | `titulo`, `parrafos: []` |
| `checks` | Lista con tildes en una columna, con notas opcionales en cursiva | `titulo`, `items: []`, `notas: []` |
| `checks2` | Lista con tildes en dos columnas | `titulo`, `items: []` |
| `tabla` | Tabla de pauta y resultados; la fila `destacada` va en naranja | `titulo`, `columnas`, `filas`, `destacada`, `nota` |
| `comparacion` | Dos tarjetas: Hoy / Con el plan | `antes: {label, texto}`, `despues: {label, texto}` |
| `precios` | Tarjeta de arranque y tarjeta de plan mensual | `arranque` y `mensual: {badge, label, monto, moneda, texto}` |
| `etapas` | 4 tarjetas de plazos | `items: [{cuando, texto}]` |
| `contacto` | Caja de contacto | `titulo`, `texto` |

Cada página lleva además:
- `indice`: el texto que aparece en el índice de la portada. Con `"indice_estilo": "items"` dentro de `portada`, el índice se muestra como ítems con descripción (`indice_desc` en cada página) en lugar de números.
- `kicker`: el rótulo chico de arriba a la izquierda.
- `color`: `blue`, `orange` o `slate`. Pinta la rayita del rótulo y los números de las secciones.
- `titulo`: usar `<br>` para el corte de línea.
- `subtitulo`: opcional, en cursiva.
- `confidencial`: opcional; agrega "CONFIDENCIAL" al pie.

Las secciones se numeran solas (01, 02…). Para mostrar un punto en lugar del número, se pone `"numero": "•"`. Para resaltar en blanco una parte del texto, se usa `<b>…</b>`.

Íconos de la portada: `meta`, `web`, `crm`, `video`, `chat`, `mail`, `star`, `search`, `camera`, `users`.
