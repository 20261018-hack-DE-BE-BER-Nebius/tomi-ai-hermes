---
id: comparison-analysis-es
topic: comparison-analysis
lang: es
title: "Análisis de vocabulario de tres comparaciones reales"
type: analysis
status: evidence-reviewed
updated: "2026-10-18"
tags: [tomi, comparison, evidence, es]
---

[EN](comparison-analysis-en.md) · [ES](comparison-analysis-es.md) · [DE](comparison-analysis-de.md) · [FR](comparison-analysis-fr.md)

> Estado de publicación: el vídeo final de entrega sigue pendiente. La transcripción automática del MOV fuente terminó (46 fragmentos, 87 segmentos); faltan la escucha y la revisión de fidelidad. La duración del vídeo provisional no certifica la publicación final.

# Análisis de vocabulario de tres comparaciones reales

Las medidas usan la página histórica completa y el artículo moderno completo citado en cada comparación acotada exitosa. Son descriptivas, no puntuaciones del modelo ni exactitud de asociación. La revisión de soporte la realizó el asistente; falta certificación humana independiente.

| Fila histórica | Artículo moderno | Palabras históricas | Palabras modernas | Jaccard | Jensen–Shannon |
|---|---|---:|---:|---:|---:|
| 13 | Shipbuilding | 1419 | 5593 | 0.109744 | 0.472972 |
| 104 | Litre | 1460 | 1903 | 0.118505 | 0.514112 |
| 115 | Textile bleaching | 1220 | 1145 | 0.096398 | 0.546280 |

El tokenizador elimina controles de diseño Parse, convierte a minúsculas y cuenta secuencias de letras Unicode. Conserva palabras frecuentes y no repara OCR, reduce raíces ni normaliza ortografía. Jaccard divide vocabulario compartido por su unión. Jensen–Shannon usa frecuencias normalizadas y logaritmo base2; esta implementación va de0 a1.

| Fila histórica | Palabra | Recuento histórico / por1000 | Recuento moderno / por1000 |
|---|---|---:|---:|
| 13 | `timber` | 2 / 1.409 | 4 / 0.715 |
| 13 | `ship` | 12 / 8.457 | 35 / 6.258 |
| 13 | `shipbuilding` | 0 / 0.000 | 41 / 7.331 |
| 104 | `litre` | 2 / 1.370 | 39 / 20.494 |
| 104 | `cubic` | 5 / 3.425 | 19 / 9.984 |
| 104 | `brit` | 33 / 22.603 | 0 / 0.000 |
| 115 | `veffel` | 4 / 3.279 | 0 / 0.000 |
| 115 | `gas` | 3 / 2.459 | 0 / 0.000 |
| 115 | `bleaching` | 2 / 1.639 | 37 / 32.314 |

## Interpretación
El caso naval compara piezas de madera con la definición de astillero, no una transición histórica demostrada. El artículo moderno es casi cuatro veces más largo; los recuentos cambian por motivos distintos del vocabulario. Litro establece continuidad terminológica limitada, sin aceptar conversiones históricas corruptas. Blanqueo compara cobertura. El token OCR veffel se conserva tal como aparece y no certifica ortografía histórica. Las palabras funcionales dominan; poca coincidencia no demuestra conocimiento nuevo.

## Soporte documental exacto
La tabla identifica posiciones Unicode, revisiones y recibos originales. Objetos de citas y hashes están en comparison-analysis.json. Los tres fallos originales de preguntas amplias siguen en reviewed-six-cases.json. No se ejecutó BERTopic ni se declara cambio causal, acuerdo completo o probabilidad calibrada.

| Source | Span | Revision | Link |
|---|---|---|---|
| britannica:309f765b1ecc83e0a7f7762e44b4a927a7555443:train:13 | 1720:2520 | 309f765b1ecc83e0a7f7762e44b4a927a7555443 | [source](https://huggingface.co/datasets/NationalLibraryOfScotland/encyclopaedia_britannica_illustrated/tree/309f765b1ecc83e0a7f7762e44b4a927a7555443) |
| wikipedia:187377 | 0:800 | 1348971360 | [source](https://en.wikipedia.org/w/index.php?oldid=1348971360) |
| britannica:309f765b1ecc83e0a7f7762e44b4a927a7555443:train:104 | 157:485 | 309f765b1ecc83e0a7f7762e44b4a927a7555443 | [source](https://huggingface.co/datasets/NationalLibraryOfScotland/encyclopaedia_britannica_illustrated/tree/309f765b1ecc83e0a7f7762e44b4a927a7555443) |
| wikipedia:18094 | 0:800 | 1341552788 | [source](https://en.wikipedia.org/w/index.php?oldid=1341552788) |
| britannica:309f765b1ecc83e0a7f7762e44b4a927a7555443:train:115 | 537:863 | 309f765b1ecc83e0a7f7762e44b4a927a7555443 | [source](https://huggingface.co/datasets/NationalLibraryOfScotland/encyclopaedia_britannica_illustrated/tree/309f765b1ecc83e0a7f7762e44b4a927a7555443) |
| wikipedia:11501704 | 0:800 | 1338304831 | [source](https://en.wikipedia.org/w/index.php?oldid=1338304831) |

`tomi-ai-hermes/evidence/comparison-analysis.json` · `tomi-ai-hermes/evidence/reviewed-six-cases.json`

[submission-guide-es](submission-guide-es.md)

[Índice de documentación](README.md) · [Instrucciones de instalación](../../README.md) · [Revisión de fuentes y exportación](source-review.json)
