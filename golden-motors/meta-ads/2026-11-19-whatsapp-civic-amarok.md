# Golden Motors · Campañas de WhatsApp: Honda Civic (Alejandro) y Amarok V6 (Renzo) (19/11/2026)

## Pedido

Dos videos del Drive (carpeta `1Mvy-XwVcOKVVg42Prv7f8uW035ykFuVX`), uno por auto, para conseguir mensajes por WhatsApp. Cada auto va al número de un vendedor: uno a Renzo y otro a Alejandro. ARS 20.000 por día cada uno. Solo ciudad de Córdoba, hombres de 30 años o más, sin "Reach more people likely to respond". Quedan en borrador para que Nahuel los revise.

## Videos (escuchados y revisados cuadro por cuadro)

| Archivo | Duración | Contenido | Video en Meta | Portada |
|---|---|---|---|---|
| Honda Civic Alejandro speaking (1).mp4 | 42 s | Alejandro presenta el auto. Textos en pantalla: Honda Civic EXS 2016 automático, 120 mil km, techo solar, cuero, cámara de retroceso, control de estabilidad desactivable, modo ECO, velocidad crucero, comandos al volante. Cierra con "Escribinos, te respondemos por mensaje" y el logo | `2642903039471101` | `14c17fa2b0aa97dd7f329b795d2465e4` |
| Amarok v6 Ale speaking.mp4 | 30 s | Alejandro presenta la camioneta. Textos en pantalla: Amarok V6 2022, Volkswagen 4×4, 57 mil km reales, services oficiales al día, "Subí el volumen, escuchá el V6". Cierra con "Escribinos" y el logo | `1105734122257478` | `6487c6b6fb87a8d745bf770790f3941f` |

- Asignación: **Civic → Alejandro** (él habla en ese video) y **Amarok → Renzo**. Ojo: Alejandro también aparece en el video de la Amarok, pero el copy no nombra a ningún vendedor, así que no hay contradicción. Se puede invertir.
- En el audio del Civic parece que Alejandro dice un precio ("23 millones"). Hay que confirmar que siga vigente. El copy no lleva precio.
- En el audio de la Amarok parece decir "primera mano". No lo puse en el copy hasta confirmarlo.

## Estructura (todo en borrador, nada publicado)

Una campaña por auto, para que cada vendedor tenga sus ARS 20.000 fijos y uno no le saque presupuesto al otro.

| | Civic · Alejandro | Amarok · Renzo |
|---|---|---|
| Campaña | `120253604751880736` GM_WA_HondaCivic2016_Alejandro_Nov26 | `120253604752410736` GM_WA_AmarokV6_2022_Renzo_Nov26 |
| Objetivo y presupuesto | Interacción, CBO ARS 20.000/día, menor costo | igual |
| Conjunto | `120253604759810736` "Cba ciudad · Hombres 30-65 · WA Alejandro" | `120253604765070736` "Cba ciudad · Hombres 30-65 · WA Renzo" |
| Optimización | Conversaciones, destino WhatsApp, página `621210564402720` | igual |
| Anuncio | `120253604778050736` 01_Civic2016_Alejandro_Video42s | `120253604778320736` 01_AmarokV6_2022_Renzo_Video30s |
| Creativo | `1771309471662176` | `1666350091558315` |

**Público (los dos conjuntos):**
- Ciudad de Córdoba (key 84740), sin radio extra.
- Solo personas que **viven** ahí ("home"), sin "recently in".
- Hombres de 30 a 65 años.
- Advantage+ audience **apagado**, porque la edad y el género tienen que ser fijos.
- Expansión de públicos (lookalike y custom audience) apagada.

**Ubicaciones:** Feed, Stories y Reels de Facebook. Feed, Stories, Reels, explore_home y profile_feed de Instagram.

**Creativo:** creado desde cero (video_data con título, mensaje, portada y botón WhatsApp). Todas las mejoras de Meta AI están en OPT_OUT. Cada auto tiene un mensaje de bienvenida y un mensaje precargado para que el vendedor sepa por qué auto le escriben.

## Copy

**Civic** · Título: "Honda Civic EXS 2016 automático" · Descripción: "Golden Motors · Córdoba"

> Honda Civic EXS 2016, automático, con 120.000 km.
>
> Viene completo: techo solar, tapizado de cuero, cámara de retroceso, control de estabilidad, modo ECO, velocidad crucero y comandos al volante.
>
> Está en nuestro local de Octavio Pinto 3181, Córdoba. Escribinos por WhatsApp y te pasamos todos los detalles para que vengas a verlo.

- Bienvenida en WhatsApp: "¡Hola! Gracias por escribir a Golden Motors. Contanos qué querés saber del Honda Civic EXS 2016."
- Mensaje precargado: "Hola, quiero info del Honda Civic EXS 2016"

**Amarok** · Título: "Amarok V6 2022 · 57.000 km" · Descripción: "Golden Motors · Córdoba"

> Amarok V6 2022, 4x4, con 57.000 km y los services oficiales al día.
>
> Subí el volumen y escuchá cómo suena el V6.
>
> La tenemos en Golden Motors, Octavio Pinto 3181, Córdoba. Mandanos un WhatsApp y te respondemos con toda la info para que vengas a verla.

- Bienvenida: "¡Hola! Gracias por escribir a Golden Motors. Contanos qué querés saber de la Amarok V6 2022."
- Mensaje precargado: "Hola, quiero info de la Amarok V6 2022"

## Pendiente

1. **Números de WhatsApp:** la API no muestra qué número usa cada conjunto (los conjuntos viejos de "Ale" y "Renzo" solo devuelven la página). Hay que elegir el número de cada vendedor en el Ads Manager, dentro de cada conjunto, o pasarme los dos números para cargarlos yo.
2. Revisar en el Ads Manager que "Reach more people likely to respond" aparezca destildado. En la API se mandaron apagados Advantage+ audience y la expansión de públicos.
3. Revisar que multi-advertiser ads aparezca apagado.
4. Al crear el creativo, la herramienta metió un `link_title` en el CTA. En Iron Bird ese campo trabó la publicación de un anuncio copiado. Si al publicar da error, se rehace el creativo.
5. Publicar solo con el OK de Nahuel: `ads_activate_entity` con los IDs de campaña, conjunto y anuncio, y después verificar en vivo.
