# Diego Díaz Motos: cuenta publicitaria

Cliente de anuncios de la agencia. Se trabaja igual que Iron Bird Fitness, Nate Velázquez y Rey La Tinta: mismos pasos, mismas skills y mismo formato de entregables (PDF con `build.py`).

## Datos de la cuenta (Meta)

| Dato | Valor |
|---|---|
| Cuenta publicitaria | `370883605163736` (act_370883605163736) |
| Business | Diego Diaz Motos (`434414456421951`) |
| Página de Facebook | Diego Díaz Motos (`434406449756085`) |
| Moneda | ARS (mercado argentino: los anuncios van en español rioplatense) |
| Estado al 4/11/2026 | Activa, con medio de pago |
| Campañas existentes | "Tornado 300 Sorteo / Website" (ARS 2.586 gastados en 90 días) y "Tornado 300 Sorteo / Website / Sec AD" (sin gasto) |

Pendiente: la página **no aceptó los términos de Lead Ads** (https://www.facebook.com/legal/leadgen/tos). Hace falta aceptarlos antes de armar campañas con formulario de leads.

## Cómo se trabaja (mismo flujo que los otros clientes)

1. **Auditoría de la cuenta**: plugin `claude-ads` (`ads-audit`, `ads-meta`, `ads-budget`) + conector Meta para leer campañas y métricas. Salida: PDF de análisis, como `nate-velazquez/analisis-anuncios/`.
2. **Estrategia y oferta**: `ads`, `offers`, `marketing-psychology`. Para motos: oferta concreta (modelo, precio o cuota, financiación, sorteo), objetivo WhatsApp o formulario.
3. **Guiones de anuncio**: `ad-creative` para gancho, mensaje principal y CTA, después `ig-human` y `copy-editing` para que no suene a IA. Se cargan en `meta-ad-scripts/build.py` (mismo diseño que Rey La Tinta: gancho, mensaje principal, llamado a la acción y nota de dirección).
4. **Creativos con IA** si no hay video propio: conector Higgsfield + `07-ecommerce-ad`, `09-product-360`, `11-social-hook`, `01-cinematic`.
5. **Edición de los videos que mande Diego**: `business-short-form-reels` o `cine-frame`, captions con `fitted-stacked-captions`.
6. **Medición**: `conversion-tracking` y `analytics` (píxel y eventos del sitio, ya que las campañas actuales van a Website).
7. **Reporte**: `ads-report`.

Regla del conector Meta: leer está bien; cualquier cambio en la cuenta (crear, pausar o cambiar presupuesto) se confirma con Nahuel antes.

## Generar el PDF de guiones

```bash
python3 diego-diaz-motos/meta-ad-scripts/build.py
```

Antes hay que completar la lista `ADS` en el script con los guiones aprobados.
