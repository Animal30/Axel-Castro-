# Golden Motors · Boost de los posteos del Toyota Yaris y la Husqvarna para WhatsApp (26/11/2026)

## Pedido
Dos campañas, una por posteo nuevo de @goldenmotorscba, para conseguir conversaciones de WhatsApp. Un número de Renzo y otro de Alejandro: **Nahuel carga los números a mano** en el Ads Manager. Público como venimos haciendo: ciudad de Córdoba, hombres 30-65+, sin "Reach more people likely to respond". No dijo qué auto va con quién: las campañas no llevan nombre de vendedor.

## Posteos
- **Toyota Yaris 1.5 XLS automático 2024** · reel de 23 s (25/11) · ID `17884748850652083` · https://www.instagram.com/reel/DgKtQyzx01b/. Texto: 79.000 km, services oficiales, cubiertas con 4.000 km. Sin precio.
- **Husqvarna Svartpilen 401 2022** · reel de 53 s (26/11) · ID `18035241404879728` · https://www.instagram.com/reel/DgNN5wgsNz6/. Texto: 45 CV, 4.600 km, service recién hecho, batería nueva, Brembo, ABS, quickshift. Dice "el precio es de **$4500 usd**": confirmar que sea el vigente.

## Armado (creado pausado con `ads_boost_ig_post`)
| | Yaris | Husqvarna |
|---|---|---|
| Campaña | `120253712935080736` GM_WA_ToyotaYaris2024_Posteo_Nov26 | `120253712938930736` GM_WA_HusqvarnaSvartpilen401_Posteo_Nov26 |
| Conjunto | `120253712935360736` | `120253712939420736` |
| Anuncio | `120253712935810736` (creativo `1150594267890344`) | `120253712940450736` (creativo `1169590805724696`) |
| Objetivo y presupuesto | Interacción, conversaciones por WhatsApp, CBO **ARS 20.000/día** (sugerido, igual que el Civic) | igual |
| Duración | 26/11 al 26/12 | igual |

Público (verificado en vivo, los dos): ciudad de Córdoba · "vive o frecuenta" (Meta normaliza así) · hombres · **edad mínima 30 y máxima 65 fijas** · Advantage+ audience y expansión apagados (sin `individual_setting`, a diferencia de las campañas del Civic y el Vento armadas en el panel) · solo celular.
Ubicaciones: Feed, Stories, Reels y **Marketplace** de Facebook; Feed, Stories, Reels, Explorar y perfil de Instagram.

## Pendiente
1. Cargar el número de WhatsApp de cada vendedor en el conjunto. La herramienta de boost no lo guarda.
2. Confirmar presupuesto (ARS 20.000/día cada una) y el precio de la Husqvarna.
3. Mensajes prefijados sugeridos: "Hola, quiero info del Toyota Yaris XLS 2024" / "Hola, quiero info de la Husqvarna Svartpilen 401".
4. Activar solo con el OK de Nahuel: campaña, conjunto y anuncio, uno por uno.

## Confirmaciones de Nahuel (26/11)
- Marketplace incluido: aplicado en los dos conjuntos con `ads_update_entity` y publicado con `ads_activate_entity` (`publish_as_active` false). Verificado en vivo: `marketplace` en facebook_positions, sin borradores pendientes, campañas siguen PAUSED.
- Presupuesto confirmado: ARS 20.000/día en cada campaña (verificado en vivo).
- Precio de la Husqvarna confirmado: $4.500 USD (el del texto del posteo).
- Mensajes prefijados de WhatsApp aprobados; los pega Nahuel. Números de WhatsApp: los carga Nahuel.
- Siguen pausadas hasta que Nahuel pida activar.

## Versión con video (anuncio común, editable) · 26/11

Nahuel no podía editar ubicaciones, anuncio ni número en los posteos promocionados (un anuncio sobre un posteo existente es de solo lectura). Se armaron dos campañas nuevas con el video cargado. **Quedan como borrador** (sin publicar) en el Ads Manager para que Nahuel cargue el número de cada vendedor y publique. Las campañas boosteadas (`120253712935080736` Yaris y `120253712938930736` Husqvarna) quedan pausadas y sin uso: descartar.

| | Yaris | Husqvarna |
|---|---|---|
| Video en Meta | `1190052226693017` (23 s) | `1692958275507545` (53 s) |
| Campaña | `120253713111930736` GM_WA_ToyotaYaris2024_Video_Nov26 | `120253713112070736` GM_WA_HusqvarnaSvartpilen401_Video_Nov26 |
| Conjunto | `120253713115140736` | `120253713115700736` |
| Anuncio | `120253713123010736` | `120253713123470736` |
| Título | Toyota Yaris XLS 2024 · 79.000 km | Husqvarna Svartpilen 401 · USD 4.500 |

- ARS 20.000/día cada una (CBO). Conversaciones por WhatsApp. Público: ciudad de Córdoba, hombres, edad 30-65 fija, Advantage+ audience apagado, solo celular. Ubicaciones: Facebook Feed, Marketplace, Stories y Reels; Instagram Feed, Stories, Reels, Explorar y perfil.
- Texto: datos del posteo (km, services, cubiertas, equipamiento, precio de la moto USD 4.500 confirmado, dirección). Botón WhatsApp. Saludo y mensaje prefijado en español cargados por plantilla (Yaris `1055848794186871`, Husqvarna `2362432821196849`).
- Meta AI y multi-advertiser apagados.
- `ads_create_creative` + `ads_create_ad` volvió a dejar `link_title` en el CTA: se reemplazó el creativo con `ads_update_entity` sin ese campo (regla: ver arriba). Borradores validados, sin errores.
- Sin número de WhatsApp: lo carga Nahuel. Al publicar, quedan ACTIVAS (el borrador está staged como ACTIVE).
- Se subió el video desde la URL del reel de Instagram; funciona, pero el primer intento del Yaris falló al copiar el link.

## Revisión después del lanzamiento (Nahuel publicó, solo lectura)
- Yaris `120253713111930736` ACTIVE, **ARS 20.000/día**, sin gasto todavía. Husqvarna `120253713112070736` ACTIVE, **ARS 24.227/día** (no 20.000; ya gastó ARS 1.054 en 228 impresiones). Conjuntos y anuncios ACTIVE, entrega "preparando".
- Público (los dos): ciudad de Córdoba, hombres, edad 30-65 fija, Advantage+ audience apagado, solo celular. Ubicación "vive, reciente y frecuenta" (Nahuel la dejó así). Facebook Feed, Marketplace, Stories y Reels; Instagram Feed, Stories, Reels, Explorar y perfil.
- Creativos publicados con el texto original de los posteos (con hashtags), sin título propio. Husqvarna dice "$4500 usd" (confirmado).
- Pendiente: confirmar que el presupuesto de la Husqvarna es el deseado; confirmar número de WhatsApp de cada vendedor en el Ads Manager (la API no lo muestra); descartar las campañas "…_Posteo_Nov26" pausadas.
