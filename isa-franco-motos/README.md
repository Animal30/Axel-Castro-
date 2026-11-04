# Isa Franco Motos: cuenta publicitaria

Cliente de anuncios de la agencia (concesionaria de motos, mercado argentino). Se trabaja igual que Iron Bird Fitness, Nate Velázquez, Michael Lenny y Diego Díaz Motos: mismos pasos, mismas skills y mismo formato de entregables (PDF con `build.py`). Todo en español rioplatense y en ARS.

## Lo que ya sabemos del negocio

Del caso de éxito (`caso-8-a-32/`):

- Antes vendía **8 motos por mes**. Tenía muchas consultas, pero la mayoría eran curiosos que preguntaban el precio y desaparecían.
- El sistema: **sitio web que filtra** (cada moto con ficha y precio; antes de hablar con un vendedor la persona dice qué moto busca, cómo la piensa pagar y cuándo la quiere) + **anuncios de Meta** llevando gente al sitio.
- Presupuesto del mes: **ARS 500.000**. Resultado: **32 motos vendidas** (x4), mismo local y mismo equipo.

Esto define el objetivo de los anuncios: no buscar consultas baratas sino consultas calificadas (modelo, forma de pago y plazo).

## Datos de la cuenta (Meta)

| Dato | Valor |
|---|---|
| Cuenta publicitaria | **PENDIENTE**: al 4/11/2026 no aparece entre las cuentas conectadas al conector de Meta |
| Página de Facebook / Instagram | PENDIENTE |
| Sitio | PENDIENTE (URL del sitio que filtra) |
| Moneda | ARS |
| Lead Ads | Revisar si la página aceptó los términos (https://www.facebook.com/legal/leadgen/tos) antes de armar campañas con formulario |

Para conectarla: Isa (o quien administre su Business) tiene que darle acceso a la cuenta publicitaria al Business o al usuario de Nahuel. Después aparece en `ads_get_ad_accounts` y se completa esta tabla.

## Cómo se trabaja (mismo flujo que los otros clientes)

1. **Auditoría de la cuenta**: plugin `claude-ads` (`ads-audit`, `ads-meta`, `ads-budget`, `ads-creative`) + conector Meta para leer campañas y métricas. Salida: PDF de análisis, como `nate-velazquez/analisis-anuncios/`.
2. **Estrategia y oferta**: `ads`, `offers`, `pricing`, `marketing-psychology`. Para motos: modelo concreto, precio o cuota, financiación, entrega o permuta. Objetivo: tráfico al sitio que filtra, WhatsApp o formulario con preguntas de calificación (modelo, forma de pago, cuándo).
3. **Guiones y copy de anuncios**: `ad-creative` (ganchos, textos principales, títulos), después `ig-human` y `copy-editing` para que no suene a IA. Se cargan en `meta-ad-scripts/build.py` (gancho, mensaje principal, llamado a la acción y nota de dirección).
4. **Creativos con IA** si no hay video propio: conector Higgsfield + `07-ecommerce-ad`, `09-product-360`, `11-social-hook`, `01-cinematic`, `12-brand-story`.
5. **Edición de los videos que mande Isa**: `business-short-form-reels`, `cine-frame` o `broll-stacked-text-edit`; captions con `fitted-stacked-captions`.
6. **Medición**: `conversion-tracking`, `analytics` y `attribution` (píxel y eventos del sitio, sobre todo el envío del filtro).
7. **Tests y reporte**: `ab-testing` para comparar ángulos, `ads-report` para el cierre del mes.
8. **Contenido orgánico del caso** (para la cuenta de Nahuel): `ig-reel`, `ig-caption`, `ig-human` (ya hecho en `caso-8-a-32/`).

Regla del conector Meta: leer está bien; cualquier cambio en la cuenta (crear, pausar o cambiar presupuesto) se confirma con Nahuel antes.

## Generar el PDF de guiones

```bash
python3 isa-franco-motos/meta-ad-scripts/build.py
```

Antes hay que completar la lista `ADS` en el script con los guiones aprobados.

## Registro de campañas

- (vacío: completar a medida que se publiquen)
