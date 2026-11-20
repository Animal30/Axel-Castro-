# Golden Motors · Campañas de WhatsApp: Honda Civic (Alejandro) y Amarok V6 (Renzo) (19/11/2026)

## Pedido

Dos videos del Drive (carpeta `1Mvy-XwVcOKVVg42Prv7f8uW035ykFuVX`), uno por auto, para conseguir mensajes por WhatsApp. Cada auto va al número de un vendedor: uno a Renzo y otro a Alejandro. ARS 20.000 por día cada uno. Solo ciudad de Córdoba, hombres de 30 años o más, sin "Reach more people likely to respond". Quedan en borrador para que Nahuel los revise.

## Videos (escuchados y revisados cuadro por cuadro)

| Archivo | Duración | Contenido | Video en Meta | Portada |
|---|---|---|---|---|
| Honda Civic Alejandro speaking (1).mp4 | 42 s | Alejandro presenta el auto. Textos en pantalla: Honda Civic EXS 2016 automático, 120 mil km, techo solar, cuero, cámara de retroceso, control de estabilidad desactivable, modo ECO, velocidad crucero, comandos al volante. Cierra con "Escribinos, te respondemos por mensaje" y el logo | `2642903039471101` | `14c17fa2b0aa97dd7f329b795d2465e4` |
| Amarok v6 Ale speaking.mp4 | 30 s | Alejandro presenta la camioneta. Textos en pantalla: Amarok V6 2022, Volkswagen 4×4, 57 mil km reales, services oficiales al día, "Subí el volumen, escuchá el V6". Cierra con "Escribinos" y el logo | `1105734122257478` | `6487c6b6fb87a8d745bf770790f3941f` |

- Asignación: **Civic → Alejandro** (él habla en ese video) y **Amarok → Renzo**. Ojo: Alejandro también aparece en el video de la Amarok, pero el copy no nombra a ningún vendedor, así que no hay contradicción. Se puede invertir.
- Precio del Civic confirmado por Nahuel el 19/11: **$23.500.000**. Se sumó al copy (creativo v2).
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
| Creativo | `1644891303786332` (v2, con precio; reemplazó a `1771309471662176`) | `1666350091558315` |
| WhatsApp | Alejandro, +54 9 3515 90-1528 (`5493515901528`) | Renzo, +54 9 3585 48-0090 (`5493585480090`) |

**Público (los dos conjuntos):**
- Ciudad de Córdoba (key 84740), sin radio extra.
- Solo personas que **viven** ahí ("home"), sin "recently in".
- Hombres de 30 a 65 años.
- Advantage+ audience **apagado**, porque la edad y el género tienen que ser fijos.
- Expansión de públicos (lookalike y custom audience) apagada.

**Ubicaciones:** Feed, Stories y Reels de Facebook. Feed, Stories, Reels, explore_home y profile_feed de Instagram.

**Creativo:** creado desde cero (video_data con título, mensaje, portada y botón WhatsApp). Todas las mejoras de Meta AI están en OPT_OUT. Cada auto tiene un mensaje de bienvenida y un mensaje precargado para que el vendedor sepa por qué auto le escriben.

## Copy

**Civic (v2)** · Título: "Civic EXS 2016 · $23.500.000" · Descripción: "Golden Motors · Córdoba"

> Honda Civic EXS 2016, automático, con 120.000 km.
> Precio: $23.500.000
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

1. ~~Números de WhatsApp~~: cargados el 19/11 en el `promoted_object` de cada conjunto (`whatsapp_phone_number`). Conviene confirmar en el Ads Manager que aparezca el número correcto en cada conjunto.
2. Revisar en el Ads Manager que "Reach more people likely to respond" aparezca destildado. En la API se mandaron apagados Advantage+ audience y la expansión de públicos.
3. Revisar que multi-advertiser ads aparezca apagado.
4. Al crear el creativo, la herramienta metió un `link_title` en el CTA. En Iron Bird ese campo trabó la publicación de un anuncio copiado. Si al publicar da error, se rehace el creativo.
5. Publicar solo con el OK de Nahuel: `ads_activate_entity` con los IDs de campaña, conjunto y anuncio, y después verificar en vivo.

## Corrección (19/11): anuncios vacíos en el Ads Manager

**Qué pasó:** `ads_create_creative` mete solo un `link_title` y un `link_description` dentro del CTA de WhatsApp, tomados del título y la descripción. Meta ya no acepta esos campos (error 1815589, "Link Title and Link Description Are Deprecated"). Por eso el Ads Manager mostraba los anuncios sin video ni copy, y el de la Amarok tenía un error de publicación. Además, el conjunto de Renzo había quedado con ubicación "vive, estuvo recientemente o frecuenta".

**Arreglo:**
- Se reemplazó el creativo de los dos anuncios por un creativo inline, cargado con `ads_update_entity` en el borrador. Tiene `video_data` con `video_id`, `image_hash` de portada, `title` y `message`, y un CTA `WHATSAPP_MESSAGE` con solo `link` y `app_destination`, sin `link_title` ni `link_description`.
- Se dejó `contextual_multi_ads` en OPT_OUT y las mejoras de Meta AI en OPT_OUT.
- El conjunto de Renzo volvió a ubicación "home" (solo gente que vive en la ciudad de Córdoba).
- Releído el borrador: los dos anuncios y los dos conjuntos quedaron sin `active_errors`.
- Se perdió el mensaje de bienvenida y el mensaje precargado de WhatsApp: venían con el creativo viejo. Se pueden cargar a mano en el Ads Manager, en la sección "Plantilla de mensaje".
- La descripción "Golden Motors · Córdoba" se sacó: Meta no la muestra en anuncios de video.

**Regla para próximas campañas:** no usar `ads_create_creative` con headline o description para anuncios de mensajes. Crear el creativo inline en `ads_create_ad` (o `ads_update_entity` en el borrador) con `video_data` armado a mano.

**Borradores que no son de esta sesión:** en la cuenta hay dos borradores creados a mano desde el Ads Manager ("Website / Catalogo" y "New Engagement Campaign"), los dos con errores. No los toqué. Nahuel decide si los descarta.

## Segunda corrección (19/11): copy invisible en las casillas del Ads Manager

- Nahuel seguía sin ver el texto principal y el título en las casillas del Ads Manager. El copy estaba guardado solo dentro de `object_story_spec.video_data`.
- Se cargó el creativo de los dos anuncios con el copy **también a nivel del creativo** (`body` y `title`), que es de donde el Ads Manager llena las casillas, además de en `video_data`.
- Botón WhatsApp con solo `link` y `app_destination` (sin `link_title`), con la portada, `contextual_multi_ads` en OPT_OUT y las mejoras de Meta AI en OPT_OUT.
- Se recuperaron el saludo y el mensaje precargado en español con plantillas nuevas: Civic `3412028115647662`, Amarok `2570280666790668`.
- Ojo: `ads_create_creative` sin `message_template` le pone a los anuncios de WhatsApp un saludo por defecto **en inglés**. Siempre hay que pasar la plantilla en español.
- Creativos de referencia ya creados en la cuenta: Civic `1680485846777761`, Amarok `40173781652266476`. Los creativos viejos (`1771309471662176`, `1644891303786332`, `1666350091558315` y `2298508254262028`) no están en uso.
- Relectura final del borrador: los dos anuncios figuran como **VALIDATED**, sin `active_errors`.

## Publicación (19/11, Nahuel la publicó desde el Ads Manager)

Revisión en vivo después de publicar:
- **Publicada solo la Amarok:** campaña `120253604752410736` ACTIVE, ARS 20.000/día. Conjunto `120253604765070736` ACTIVE. Anuncio `120253604778320736` en revisión (IN_PROCESS, todavía sin entrega). Creativo publicado `1165249865980242`: copy, título, video, portada y botón WhatsApp correctos.
- **El Civic no está publicado:** la campaña `120253604751880736` sigue en borrador. Nahuel pensaba que los dos anuncios estaban en una sola campaña, pero en la cuenta hay un solo anuncio activo.
- **Error grave en el conjunto publicado:** la ubicación quedó en **toda Argentina** (countries AR, con home, recent y frequently_in), no en la ciudad de Córdoba. Edad 30-65, hombres y Advantage+ audience apagado quedaron bien.
- Ubicaciones: se sumaron Marketplace y el feed de perfil de Facebook, que no estaban en el plan.
- El `promoted_object` no muestra el número de WhatsApp por API. Hay que confirmarlo en el Ads Manager.
- Propuesto a Nahuel (espera su sí): corregir la ubicación a la ciudad de Córdoba, solo "vive" (y opcionalmente sacar Marketplace y el feed de perfil de Facebook), volver a publicar el conjunto, y publicar la campaña del Civic.

## Revisión de solo lectura (19/11, después de que Nahuel editó desde el Ads Manager)

Nahuel pidió que no toque nada. Estado en vivo:
- **Dos campañas de la Amarok activas a la vez:**
  1. `120253604752410736` "GM_WA_AmarokV6_2022_Renzo_Nov26": Interacción, ARS 20.000/día. Anuncio en revisión (creativo `2701359420308541`, copy correcto). **La ubicación sigue en toda Argentina** (home, recent y frequently_in), con Marketplace y el feed de perfil de Facebook.
  2. `120253607809590736` "Amarok V6 2022" (creada por Nahuel): **Tráfico**, ARS 7.000/día, optimiza conversaciones por WhatsApp. Ciudad de Córdoba, pero con "vive, estuvo recientemente o frecuenta". **Advantage+ audience prendido**: edad mínima fija de 18 (el rango 30-65 queda solo como sugerencia), y género e interés "Automobiles" también como sugerencia. Creativo `1468765791874154` = posteo de Instagram con otro copy ("Volkswagen Amarok 3.0 V6 Comfortline… Diésel, Cabina doble"), sin título.
- **El Civic no tiene ninguna campaña publicada.**
- Mensajes prefijados y número de WhatsApp: la API no los muestra en anuncios publicados. Hay que mirarlos en el Ads Manager.

## Revisión de solo lectura #2 (19/11, después de que Nahuel publicó el Civic)

- **Civic** `120253604751880736`: ACTIVE, ARS 20.000/día. Anuncio en revisión (creativo `1003796589470863`, copy, título, video y botón correctos). Conjunto: ciudad de Córdoba, hombres 30-65 fijos, Advantage+ audience apagado. Ubicación con "vive, reciente y frecuenta". Suma Marketplace y el feed de perfil de Facebook.
- **Amarok (Renzo, video)** `120253604752410736`: ACTIVE, ARS 20.000/día, anuncio **aprobado y preparando la entrega**. **La ubicación SIGUE en toda Argentina.** Urgente.
- **Amarok V6 2022 (posteo)** `120253607809590736`: Tráfico, ARS 7.000/día, aprobado. **Advantage+ audience sigue prendido** (edad mínima fija 18; 30-65 y género como sugerencia) e interés Automobiles. Ubicación ciudad de Córdoba, con vive, reciente y frecuenta.
- Ningún conjunto excluye seguidores. Que los videos sean anuncios sin publicar en el perfil (dark posts) no los saca de los seguidores.
- Total diario si todo entrega: ARS 47.000 (Amarok 27.000 entre dos campañas, Civic 20.000).

## Revisión de solo lectura #3 (19/11)

- **Amarok (Renzo, video):** el cambio a la ciudad de Córdoba que hizo Nahuel quedó como **borrador sin publicar** (draft "modify" en el conjunto `120253604765070736`). Lo publicado sigue en toda Argentina, y el anuncio está aprobado y preparando la entrega. Falta que Nahuel apriete "Publicar" en el Ads Manager.
- **Amarok V6 2022 (posteo):** corregido. Advantage+ audience apagado, hombres 30-65 fijos, ciudad de Córdoba (vive, reciente y frecuenta), interés Automobiles. Anuncio en revisión otra vez por la edición.
- **Civic:** aprobado y preparando la entrega. Ciudad de Córdoba, hombres 30-65 fijos, Advantage+ audience apagado.

## Corrección publicada (19/11, con OK de Nahuel)

- Conjunto `120253604765070736` (Amarok de Renzo): targeting cargado como ciudad de Córdoba (84740), location_types "home", hombres, 30-65, Advantage+ audience y relaxation apagados, mismas ubicaciones. Publicado con `ads_activate_entity` (object_ids solo el conjunto).
- **Verificado en vivo:** ciudad de Córdoba, hombres 30-65, Advantage+ audience apagado. Meta guardó location_types como `home` + `frequently_in`: lo normaliza así, sin "recent". Toda Argentina quedó eliminada. Borrador vacío.
- El conjunto quedó IN_PROCESS (Meta revisa el cambio antes de entregar).

## Resultados primeras ~30 h (19/11 tarde y 20/11 parcial)

| Campaña | Gasto ARS | Conversaciones WA | Costo/conv | Alcance | Frec. | CTR | CPM |
|---|---|---|---|---|---|---|---|
| Civic, Alejandro (20.000/día) | 14.592 | 16 | 912 (20/11: 612) | 2.332 | 1,45 | 4,09% | 4.320 |
| Amarok, Renzo, video (20.000/día) | 10.851 | 11 | 986 (20/11: 1.161) | 1.491 | 1,38 | 3,02% | 5.280 |
| Amarok V6 2022, posteo (7.000/día) | 5.688 | 7 | 813 | 609 | 1,62 | 4,67% | 5.775 |
| **Total** | **31.131** | **34** | **~916** | | | | |

- El video del Civic retiene bien: 573 reproducciones de 25% y 495 ThruPlay sobre 3.378 impresiones.
- Amarok de Renzo: ~ARS 550 (5%) se gastaron fuera de Córdoba, en el rato antes de la corrección. Desde el arreglo, todo va a Córdoba.
- En 2025, la misma cuenta pagaba entre ARS 290 y 990 por conversación (con pesos de 2025). ~ARS 900 hoy está en línea.
- Recomendación: no tocar nada hasta tener 5-7 días de datos (fase de aprendizaje). Pedir a Renzo y Alejandro cuántas consultas son reales y cuántas avanzan.
