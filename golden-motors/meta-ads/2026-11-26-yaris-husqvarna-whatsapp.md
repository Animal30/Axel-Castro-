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
