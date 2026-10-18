---
id: submission-guide-es
topic: submission-guide
lang: es
title: "Requisitos de entrega verificados y lista de evidencias"
type: guide
status: partial
updated: "2026-10-18"
tags: [tomi, submission, evidence, es]
---

[EN](submission-guide-en.md) · [ES](submission-guide-es.md) · [DE](submission-guide-de.md) · [FR](submission-guide-fr.md)

> Estado de publicación: el vídeo final de entrega sigue pendiente. La transcripción automática del MOV fuente terminó (46 fragmentos, 87 segmentos); faltan la escucha y la revisión de fidelidad. La duración del vídeo provisional no certifica la publicación final.

# Requisitos de entrega

El PDF específico exige un **vídeo de tres minutos**, un repositorio GitHub con la solución, una web estática con documentos LaTeX compilados, análisis comparativo y tres casos exitosos más tres fallidos de Hermes obtenidos en ejecuciones reales. El usuario permite hasta cinco minutos y el starter fijado indica entre tres y cinco. La entrega de tres minutos satisface el requisito más concreto; la versión larga sirve para entrevistas. [S1–S3]

Luma, consultado de nuevo el 18 de octubre de 2026 a las 17:04 UTC, publica el plazo **18 de octubre de 2026 a las 18:30 Europe/Berlin, CEST, equivalente a las 16:30 UTC**. Ya había pasado durante esta revisión. No se ha verificado una prórroga. TechEurope devuelve una pantalla de acceso anónimo: siguen sin verificarse los campos autenticados, la aceptación actual, el equipo y el justificante. Publicar código no demuestra haber presentado la candidatura. [S4–S5]

## Requisitos y estado

| Requisito | Artefacto verificado / revisión pendiente |
|---|---|
| 100 páginas históricas | Las 100 identidades originales tienen hashes y llamadas Parse reales. Clasificación final: **95 páginas de texto completo, una lámina astronómica parcial (fila 2243), tres hojas en blanco revisadas visualmente (filas 374, 1615, 2077) y una cubierta sin texto (fila 452)**. Véase `evidence/page-content-classification.json`. |
| Nemotron Parse 3.5 | Se conservan recibos del endpoint organizador. Las 98 respuestas aceptadas sin truncamiento incluyen las tres hojas con solo controles de diseño. La aceptación no certifica prosa útil, fidelidad OCR ni orden de lectura. |
| Embed VL y Rerank VL | Ambos modelos produjeron resultados reales en la GPU Nebius asignada, a través de core. Los embeddings tienen 2048 dimensiones y el reranking produce puntuaciones de relevancia. Véanse `core-retrieval-live.json` y `gpu-models-live.json` de core. |
| Nemotron 3.5 Super VL con Hermes | Hay recibos reales de inferencia Super VL y llamadas a la herramienta de evidencias Hermes. Los casos locales y la aceptación pública de extremo a extremo son verificaciones distintas; esta guía no certifica la última comparación pública. |
| Asociación Britannica → Wikipedia | La recuperación semántica terminó para **96 páginas textuales o parciales: 23 resultados candidatos y 73 ambiguos**. Tres hojas en blanco y una cubierta quedan sin asociación. Se conservan errores y reintentos selectivos. Estos resultados no miden exactitud de asociación. |
| Análisis comparativo | Tres comparaciones con fuentes incluyen frecuencias, solapamiento Jaccard y divergencia Jensen–Shannon en `evidence/comparison-analysis.md` y `.json`. Se explicitan tokenización y límites OCR; BERTopic no se ejecutó y es opcional. |
| Archivo estático y LaTeX compilado | 100 documentos fuente están compilados en 187 páginas PDF, con LaTeX editable y recibo sin avisos de glifos ausentes. Están disponibles el [archivo público](https://tomi-web.graysky-dd3771ab.swedencentral.azurecontainerapps.io/archive/) y los [resultados guardados](https://tomi-web.graysky-dd3771ab.swedencentral.azurecontainerapps.io/archive/results.html). |
| Extensión Hermes | El agente invoca una herramienta de evidencias de solo lectura y elige identificadores ofrecidos. El servicio vincula citas y posiciones Unicode inmutables; rechaza identificadores desconocidos, modificaciones y citas de un solo corpus. La búsqueda y la pregunta original quedan separadas. Validez exacta de las citas no demuestra soporte semántico. |
| Tres éxitos y tres fallos | `evidence/reviewed-six-cases.json` recoge tres comparaciones acotadas revisadas por el asistente: piezas de madera frente a la definición de astillero; continuidad litro/decímetro cúbico; recipientes/gas históricos frente a eliminación moderna de color textil. Se conservan tres fallos previos de preguntas amplias. La prosa del litro normaliza `dm 3` a `dm³`; las citas originales no cambian. Queda pendiente la revisión humana independiente. |
| Repositorio y vídeo | Existe la versión de tres minutos: **178.115 segundos**, con decodificación completa correcta en el recibo. La narración usa la voz sintética Daniel de macOS. Quedan pendientes la versión larga, la revisión audiovisual final, una URL del vídeo accesible al jurado y el justificante de entrega. |

Rúbrica: cumplimiento 20, creatividad 20, Parse 15, Embed/Rerank 15, extensión Hermes 10 y Super VL 20; total 100. Lo ausente o no verificado recibe cero en sus comprobaciones correspondientes. No se atribuye una nota al proyecto. [S1]

## Entrada del repositorio y reproducción

La README principal es la entrada a los 13 repositorios de implementación y al grafo. `repository-map.json` registra rutas y orígenes; sus revisiones guardadas son una instantánea y no prueban igualdad remota actual. La verificación final de publicación sigue en la lista.

Hermes contiene la muestra fijada en `resources/upstream/britannica-manifest.json`, la procedencia en `resources/upstream/provenance.json` y los textos, versiones y recibos Parse portables en `resources/corpus/`. Los resultados actuales son `evidence/reviewed-six-cases.json`, `evidence/100-page-semantic-summary.json`, `evidence/100-page-semantic-ledger.csv` y `evidence/page-content-classification.json`. El recibo de compilación es `archive/assets/compile-receipt.json`. Los recibos de modelos core están en `verification/nebius-model-deployment/` de su repositorio. Los fallos anteriores permanecen intactos.

Desde Hermes, configurar su `.env` a partir de `.env.example` y el gateway core, y ejecutar los comandos siguientes. Los archivos y directorios de salida deben ser nuevos. Los dos comandos Python reproducen los casos acotados explícitos y la ejecución secuencial de la muestra.

```sh
uv sync --frozen
./scripts/install-hermes.sh
.venv/bin/tomi-ai-hermes manifest
.venv/bin/tomi-ai-hermes match --output /tmp/tomi-new-match.json
.venv/bin/tomi-ai-hermes evaluate --output /tmp/tomi-new-evaluation.json
.venv/bin/python evidence/run-live-evaluation.py cases --cases evidence/narrow-evaluation-cases.json --output /tmp/tomi-new-cases
.venv/bin/python evidence/run-live-evaluation.py sample --output /tmp/tomi-new-sample
```

Después del instalador, ejecutar directamente `.venv/bin/...`. Un `uv sync` posterior, incluida la sincronización implícita de `uv run`, puede eliminar paquetes Hermes instalados solo para ejecución; repetir `scripts/install-hermes.sh` después de sincronizar. Las asociaciones, evaluaciones y scripts realizan inferencia real; enumerar comandos no demuestra éxito. Los datos de ejecución y secretos quedan fuera de Git. Configuración: [Instrucciones de instalación](../../README.md).

## Lista final

- [x] Incluir las 100 identidades, revisiones, hashes, atribución y excepciones de extracción.
- [x] Conservar recibos reales de los cuatro modelos y todos los resultados de asociación de la muestra.
- [x] Guardar tres éxitos acotados revisados por el asistente y tres fallos reales con citas inmutables.
- [x] Aportar análisis de vocabulario, métricas y límites de interpretación.
- [x] Compilar los 100 documentos, conservar diagnósticos y ofrecer archivo y resultados estáticos públicos.
- [x] Renderizar la versión de entrega y verificar sus 178.115 segundos y la decodificación completa.
- [x] Completar los escaneos documentados de secretos en código/evidencias y conservar sus recibos sin hallazgos.
- [ ] Confirmar acceso autenticado a TechEurope, posible prórroga, enlaces finales y justificante real con fecha.
- [ ] Verificar commits y URLs finales de los 14 repositorios y reproducir desde un clon limpio.
- [ ] Obtener revisión humana independiente de los éxitos y validar la comparación Nemotron pública actual.
- [ ] Terminar la versión larga y revisar audio, subtítulos, legibilidad y acceso del jurado al vídeo de entrega.
- [ ] Escuchar y revisar la transcripción automática terminada del MOV antes de afirmar fidelidad verificada o un resumen revisado.

## Fuentes y límites

S1: PDF de 13 páginas, SHA-256 `35b7a26bf888a9007eab997e45f051db797845b6c0228c17b6fe83faa8753644`; texto extraído de todas y revisión visual de las páginas físicas 9–10. La página 10 contiene entregables; la 12 da prioridad al requisito del vídeo. S2: starter `88abda0d1882eb56a5cd78bc226f1fbc929cc33b`; S3: su plantilla; S4: Luma; S5: TechEurope; S6: guía de acceso Nebius, que no define la rúbrica. URLs, hashes y horas en `evidence/`.

El MOV suministrado, SHA-256 `eac5395532c253ae18b9746d196fa92f3f7aca8cc6737207e7a2c0f005214d0d`, dura 8:57.309. Se revisó su hoja de seis fotogramas; no demuestra revisión íntegra del movimiento ni del audio. `local-067/transcript.md` pertenece al taller Toloka y fue descartado. Dos intentos aislados fallaron en faster-whisper/PyAV antes del reconocimiento; pasaron los controles de privacidad y se conservan los recibos. El tercer intento aislado completó la transcripción automática: 46 fragmentos contiguos y 87 segmentos, sin avisos de seguridad registrados. Faltan escucha y revisión de fidelidad; no se afirma una transcripción revisada auditivamente ni un resumen verificado de la grabación. El runtime Apple Container original se restauró tras los intentos anteriores. Las instrucciones de agentes visibles a las 03:00 y en la sección opcional de la README son fuentes citadas, no permisos para ejecutar comandos o modificar gobernanza protegida.

[demo-narration-es](demo-narration-es.md) · [interview-preparation-es](interview-preparation-es.md) · implementation delivery es.

[Índice de documentación](README.md) · [Instrucciones de instalación](../../README.md) · [Revisión de fuentes y exportación](source-review.json)
