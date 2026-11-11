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

## Registro de campañas

- **4/11/2026: "Tornado 300 Sorteo / Website / 2 Copies"** (campaña `120250612194220753`). Objetivo Tráfico, optimiza visitas a la página de destino. ARS 7.000 por día, toda Argentina, 18+, Advantage+ Audience y ubicaciones automáticas. Dos anuncios de video (mismo video y portada que el original), botón "Ver detalles" a `https://diegodiazmotos.com/`, publicados desde la página y el Instagram de Diego (IG `17841455180465545`):
  - Anuncio `120250612201820753`, "Copy A Precio": "Con $10.000 podés llevarte esta Honda XR 300 Tornado 0km". Título: "Tu Tornado 0km puede salirte $10.000". Descripción: "Sorteo 24/12 ante escribano".
  - Anuncio `120250612323720753`, "Copy B Navidad": "Este 24 de diciembre, tu regalo de Navidad puede ser una Honda XR 300 Tornado 0km". Título: "Ganate una Tornado 0km esta Navidad". Descripción: "En vivo y ante escribano".
  - Nota: el formato con varios textos en un solo anuncio (asset_feed_spec) no se publicó por el conector y en el Administrador se veía sin video. Por eso se armó como dos anuncios de video separados.
- Borrador sin publicar en la campaña original: "Tornado 300 Sorteo / Website / Copy B" (anuncio `120250611863710753`), con el copy de precio.

- **9/11/2026: rechazos y dos campañas nuevas.** Meta rechazó "Tornado 300 Sorteo / Website", "Copy A Precio" y "Copy B Navidad" (para Meta, un sorteo con números pagos es lotería, y anunciarla requiere su autorización previa). Sigue activo "Tornado 300 Sorteo / Website / Sec AD", que usa la misma pieza que el original rechazado. Se publicaron dos campañas nuevas, cada una de ARS 15.000 por día, en toda Argentina, optimizadas para visitas a la página de destino, con el mismo video y la web visible abajo:
  - "Tornado 300 / Variación Directa / Website" (campaña `120250683395140753`, anuncio `120250683397460753`). Título: "Honda XR 300 Tornado 0km".
  - "Tornado 300 / Variación Confianza / Website" (campaña `120250683395350753`, anuncio `120250683397510753`). Título: "En vivo y ante escribano, 24/12".
  - Los títulos no dicen "sorteo", pero el texto lo menciona una vez, de forma clara. Para anunciar el sorteo sin rechazos, el camino es la autorización de Meta para juegos de azar, presentando el permiso de la lotería provincial.

- **11/11/2026: cuenta publicitaria deshabilitada** (DISABLED, "actividad inusual, confirmar la información de la cuenta"), después de los rechazos por el sorteo. Próximo paso: pedir revisión desde Calidad de la cuenta (business.facebook.com/accountquality) y completar la verificación. No abrir una cuenta publicitaria nueva para seguir anunciando mientras esta esté restringida (Meta lo trata como evasión, y puede escalar al Business y a los perfiles administradores). Si la recuperan: solo campañas de venta de motos, sin sorteo.
