# Proyecto de Nahuel Casartelli: agencia de contenido y marketing

Nahuel (argentino, habla español, inglés, francés e italiano) maneja una agencia de contenido y anuncios para clientes, y además su propia cuenta de idiomas en Instagram, @iamaegene. Hablale en español rioplatense, salvo que el entregable tenga que ser en otro idioma.

## Regla principal: elegí vos las skills, en cada pedido

Nahuel no conoce los nombres de las más de 100 skills de este proyecto, y no tiene por qué conocerlos. En **cada** tarea:

1. **Antes de trabajar**, revisá la lista de skills disponibles (las del proyecto en `.claude/skills/`, el plugin claude-ads y las del sistema) y elegí las que mejor sirven para el pedido. Usá la tabla de abajo como guía, pero mirá la lista completa: puede haber una que encaje mejor.
2. **Decile en una línea cuáles vas a usar y por qué.** Ejemplo: "Uso `ig-reel` para el guion y `ig-human` para que no suene a IA." Si hay una alternativa que valga la pena, nombrala en una línea más.
3. **Usalas sin pedirle permiso** cuando el pedido es claro. Preguntá solo si dos caminos dan resultados muy distintos (por ejemplo, qué estilo de edición).
4. **Encadená skills** cuando el trabajo lo pide: investigar, escribir, humanizar, publicar.
5. Si ninguna skill encaja, hacelo igual con tu mejor criterio y decíselo.

## Mapa rápido: tipo de tarea → skills

| Si pide… | Usá |
|---|---|
| **Editar un video vertical** (reel, short) | Elegí el estilo: `business-short-form-reels`, `personal-short-form-reels`, `cine-frame`, `broll-stacked-text-edit`, `glass-explainer-reel`, `explainer-panel-reel`, `depth-ui-reel`, `split-reel`, `cutout-backdrop-reel`, `cutout-grid-reel`, `image-cluster-reel`, `visual-essay-reel`, `ranking-format`. Captions: `fitted-stacked-captions`. Motor: `hyperframes:*` |
| **Video largo de YouTube** | `educational-youtube-editor`, `lesson-doc-builder`, `split-screen-document-plus-animations` |
| **Clips de una llamada, un podcast o un video largo** | `coaching-call-clips`, `youtube-clips`, `ig-repurpose`, `video-to-written-content` |
| **Guion de reel o hooks** | `ig-reel`, después `ig-human` |
| **Carrusel** | `ig-carousel` |
| **Caption, historias, comentarios, DMs** | `ig-caption`, `ig-story`, `ig-comment`, `ig-reply`, `ig-dm` |
| **Perfil, bio, plan semanal, análisis** | `ig-profile`, `ig-plan`, `ig-audit`, `ig-viral` |
| **Estrategia de contenido o redes** | `content-strategy`, `social`, `marketing-ideas` |
| **Anuncios de Meta, Google o TikTok** (estrategia y copy) | `ads`, `ad-creative`, `marketing-psychology` |
| **Auditar cuentas de anuncios o plata desperdiciada** | plugin `claude-ads` (`ads-audit`, `ads-meta`, `ads-google`, `ads-tiktok`, `ads-budget`, `ads-report`…) |
| **Imagen o video con IA** | Conector Higgsfield (`generate_image`, `generate_video`) + skills de prompts: `01-cinematic` … `15-real-estate`, `11-social-hook`, `07-ecommerce-ad`, `12-brand-story`; también `image`, `video` |
| **Flujo UGC completo en higgsfield.ai** | `ugc-video-auto`, `higgsfield-image-auto`, `seedance-auto-generate` (necesitan Playwright y una sesión abierta en Higgsfield; solo andan en la compu de Nahuel) |
| **Oferta, precios, propuesta para un cliente** | `offers`, `pricing`, `product-marketing`, `sales-enablement` |
| **Guiones de venta, setter, objeciones** | `sales-enablement`, `copywriting`, `cold-email`, `prospecting` |
| **Imán de leads o PDF gratis** | `lead-magnets`, `copywriting`, `anthropic-skills:pdf` |
| **Buscar negocios locales o armar listas de leads** (Google Maps: nombre, teléfono, email, web, rating) | `google-maps-scraper` (comandos `/scrape`, `/scrape-batch`, `/scrape-setup`, `/scrape-jobs`; el kit está en `google-maps-scraper/`, necesita Docker; `--lang es` para Argentina), después `prospecting` y `cold-email` para el contacto |
| **Emails o secuencias** | `emails` |
| **Landing page o web** | `copywriting`, `cro`, `signup`, `seo-audit`, `ai-seo`, `schema` |
| **Plan de marketing completo** | `marketing-plan`, `customer-research`, `competitor-profiling` |
| **Decisión estratégica difícil** | `marketing-council` |
| **Lanzamiento** | `launch`, `offers` |
| **Comunidad, influencers, referidos** | `community-marketing`, `influencer-marketing`, `referrals` |
| **Medición, píxel, conversiones** | `analytics`, `conversion-tracking`, `attribution` |
| **Corregir un texto o que no suene a IA** | `copy-editing`, `ig-human` |
| **Efectos de sonido (SFX) para un video** | `sfx-library` (la biblioteca de efectos de la agencia en `sounds/library`; si todavía no está construida, se construye en la compu de Nahuel con su `build.py`) + `real-sfx` (los coloca; apuntarlo a la biblioteca con `setup.py add-library agencia <repo>/sounds/library --tier main --index`; sin biblioteca propia solo tiene los 78 de interfaz de uisfx: la primera vez correr `python scripts/setup.py init --uisfx` desde la carpeta de la skill), `earshot` (sonidos hechos con código y para medir el audio; instalarlo si falta: `git clone https://github.com/Leonxlnx/earshot` y `pip install numpy scipy soundfile soxr` + `pip install --no-deps .`). Efectos bajos, solo en los cambios de escena importantes, no en cada corte. Mostrar siempre la versión sin y con efectos |
| **Documento, PDF, presentación, planilla** | `anthropic-skills:pdf`, `anthropic-skills:docx`, `anthropic-skills:pptx`, `anthropic-skills:xlsx`; página para compartir: Artifact |

## Clientes y marcas

- Perfiles de marca para la edición: `.claude/creator-profile/<cliente>/` (`nahuel`, `nahuel-espanol` = @iamaegene, `nate`). Antes de editar para un cliente, leé su `profile.json` y su `NOTES.md`.
- Carpetas por cliente en la raíz: `nate-velazquez/`, `rey-la-tinta/`, `iron-bird-fitness/`, `latonnya/`, `nahuel-espanol/`.
- Los guiones y documentos para clientes se generan como PDF con un `build.py` en la carpeta del cliente (mirá `nate-velazquez/nutrition-tips/build.py` como modelo).
