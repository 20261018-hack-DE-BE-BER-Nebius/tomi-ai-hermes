---
id: interview-preparation-es
topic: interview-preparation
lang: es
title: "Veinte preguntas de NVIDIA y Nebius con respuestas respaldadas"
type: guide
status: conditional-draft
updated: "2026-10-18"
tags: [tomi, interview, evidence, es]
---

[EN](interview-preparation-en.md) · [ES](interview-preparation-es.md) · [DE](interview-preparation-de.md) · [FR](interview-preparation-fr.md)

> Estado de publicación: el vídeo final de entrega sigue pendiente. La transcripción automática del MOV fuente terminó (46 fragmentos, 87 segmentos); faltan la escucha y la revisión de fidelidad. La duración del vídeo provisional no certifica la publicación final.

# Preparación de la entrevista

Son preguntas probables, no una entrevista proporcionada por el organizador. Las respuestas describen la base verificada; actualizar los pendientes únicamente con recibos reales. Requisitos: [submission-guide-es](submission-guide-es.md). Evidencias de aplicación: implementation delivery es.

1. **¿Qué problema resuelve Tomi?** Tomi compara Britannica histórica con una instantánea Wikipedia fijada. Vincula diferencias o continuidad acotadas a fragmentos inspeccionables y registra cuándo las fuentes no permiten responder una pregunta amplia.

2. **¿Qué aportó el equipo además del starter?** Construimos pipeline Python, herramienta Hermes y vinculación de citas, gateway y backend Rust, interfaces multilingües, corpus reproducible y archivo LaTeX compilado. Reparamos fallos reales de almacenamiento, recuperación y protocolo, conservando sus recibos.

3. **¿Por qué los cuatro modelos Nemotron?** Parse 3.5 transforma escaneos en texto con estructura. Embed VL genera vectores normalizados de 2048 dimensiones y LanceDB los busca. Rerank VL reevalúa relevancia mediante logits. Super VL dirige la conversación Hermes y redacta comparaciones. Los cuatro tienen evidencias reales y funciones complementarias.

4. **¿Por qué Nebius?** Nebius ofrece servicios distintos: Parse e índice Wikipedia compartidos, Token Factory para Super VL y GPU asignada para Embed/Rerank. Azure aloja la aplicación. Despliegues y credenciales son independientes.

5. **¿Cómo seleccionasteis las 100 páginas?** El manifiesto fija 100 filas de 2.573 mediante muestreo aleatorio sin reemplazo y semilla 20261016. Incluye revisión inmutable y hash de cada imagen. Las páginas difíciles, blancas e ilustradas permanecen en la muestra.

6. **¿Funcionaron las 100?** Las 100 recibieron llamadas Parse. Balance final:95 páginas de texto completo,1 lámina parcial,3 hojas en blanco confirmadas visualmente y 1 cubierta sin texto. Las 98 respuestas completas aceptadas incluyen las 3 salidas con solo diseño; aceptación nunca significó OCR perfecto.

7. **¿Cómo medís la extracción?** Comprobamos hashes, procedencia, truncamiento y algunos escaneos. Tres salidas normalizadas vacías se contrastaron con las imágenes y clasificaron en blanco. No medimos una tasa de error de caracteres ni exactitud de lectura completa con etiquetado humano.

8. **¿Por qué no basta el título?** Recuperamos artículos completos de la instantánea fijada, verificamos hashes y eliminamos controles de diseño solo en entradas de modelos; después usamos Embed, LanceDB y Rerank. Un artículo ya verificado del mismo snapshot con título exacto complementa la baja recuperación BM 25. El texto original de citas no cambia.

9. **¿Cuál es vuestra precisión?** No tenemos exactitud defendible contra un conjunto etiquetado. Informamos puntuaciones, márgenes, ambigüedad, cobertura y ejemplos revisados por separado. La ejecución de 100 páginas y los reintentos conservan fallos, sin convertir respuestas API en exactitud.

10. **¿Para qué LanceDB?** LanceDB almacena documentos y vectores propios; BM 25 compartido es independiente. Verificamos escritura Azure Blob porque Azure Files no permite commits Lance seguros. La prueba inicial de 183 documentos sin vectores es histórica; los recuentos posteriores tienen sus propios recibos.

11. **¿Qué análisis realizáis?** Calculamos solapamiento Jaccard, divergencia Jensen–Shannon y frecuencias. Describen distribuciones textuales, no verdad histórica. OCR, palabras frecuentes, longitud y cobertura desigual pueden dominarlas. BERTopic era opcional y no se declara una ejecución.

12. **¿Qué hace agente a Hermes?** Hermes ejecuta un ciclo real dirigido por modelo: Super VL llama a la única función de evidencias de lectura, recibe fragmentos acotados y devuelve identificadores en afirmaciones estructuradas. Conservamos la traza. No hay herramientas de shell, archivos o navegador; después se valida la fuente de forma determinista.

13. **¿Cómo evitáis citas inventadas?** Solo pueden seleccionarse identificadores ofrecidos. El servidor los vincula a citas y posiciones Unicode inmutables y aplica el validador estricto. Se rechazan IDs desconocidos, modificaciones y citas de un solo corpus. Revisamos aparte si el fragmento sostiene realmente la afirmación.

14. **¿Qué fallos evaluáis?** Los tres fallos seleccionados son preguntas amplias navales, de medición y blanqueo: baja recuperación, políticas en vez de definiciones y OCR corrupto impidieron comparaciones completas útiles. Conservamos también página ausente, GPS imposible e inyección. Los éxitos acotados posteriores no borran esos fallos.

15. **¿Cómo tratáis la inyección de instrucciones?** OCR y texto recuperado son datos no confiables. El agente no recibe claves y dispone de una sola herramienta acotada de lectura. Las inyecciones reales provocaron abstención; regresiones rechazan referencias no autorizadas. Son pruebas de defensas concretas, no inmunidad universal.

16. **¿Qué funciona públicamente?** La base pública guardada verificó streaming Astra, siete fuentes, redirección, cancelación, eventos guardados y cierre de sesión. La ruta Hermes de cuatro modelos tiene ejecuciones y casos revisados separados. Su aceptación pública es otra comprobación de versión, no se infiere del resultado Astra.

17. **¿Qué multimodalidad habéis probado?** Las rutas públicas devolvieron PNG real y emitieron sesión realtime. Emitir una sesión no demuestra captura, reproducción ni conversación de voz. No declaramos interacción física audiovisual ni diarización sin el recibo independiente de aceptación vigente.

18. **¿Cómo es el despliegue y la seguridad?** Seis servicios están en Azure y solo la web es pública; la recuperación exigida funciona en Nebius. Las claves de proveedor permanecen en core. Los escaneos revisados están limpios. Persisten rol PostgreSQL administrativo e historial Covenant efímero; no hay aprobación de producción ni LTS.

19. **¿Qué mejoraríais después?** Prioridades: etiquetas independientes de relevancia, revisión OCR y segmentación, calibración, preguntas amplias más robustas y rol restringido de base de datos. Las hojas en blanco demuestran que transporte correcto y contenido útil se evalúan aparte.

20. **¿Está terminado y presentado?** Tres casos acotados tienen revisión de soporte por el asistente y tres fallos reales se conservan. La muestra tiene registro y reintentos separados; falta certificación humana independiente. Publicar código y vídeo no es justificante. El plazo fue 18 octubre 2026 a 18:30 CEST; prórroga y aceptación siguen sin verificar.

Referencias: `submission-guide/evidence/source-review.json`; Hermes `evidence/100-page-extraction.json`, `page-visual-review.json`, `six-case-evaluation.json`, `azure-blob-runtime-probe.json`; backend `verification/public-acceptance.json`, `public-multimodal.json`; IaC `verification/security-deployment-review.json`. Repositorios y rutas en `submission-guide/repository-map.json`. Separar prueba actual, implementación y trabajo previsto.

`Hermes/evidence/reviewed-six-cases.json`; `Hermes/evidence/live-nemotron-matching-20261018T1742Z/progress.json`; `core/verification/nebius-model-deployment/core-retrieval-live.json`; `core/verification/nebius-model-deployment/gpu-models-live.json`.

Clasificación semántica final:95 páginas con texto Parse,1 lámina astronómica parcial(fila2243),3 hojas en blanco(filas374,1615,2077) y1 cubierta sin texto(fila452)=100 originales. Se inspeccionaron visualmente las tres hojas. Las98 respuestas Parse completas aceptadas incluyen esas3 hojas con solo controles; aceptación no equivale a prosa útil ni exactitud OCR. Se conservan recibos. `Hermes/evidence/page-content-classification.json` contiene100 identidades y hashes.


Las 100 páginas originales están contabilizadas. La recuperación semántica real terminó para 96 páginas con texto o parciales:23 resultados candidatos y 73 ambiguos. Tres hojas en blanco y una cubierta sin texto quedan sin asociación; la lámina astronómica parcial está entre las 96. Se conservan fallos originales y reintentos selectivos. Estos recuentos no miden exactitud de asociación.

`Hermes/evidence/100-page-semantic-summary.json` · `Hermes/evidence/100-page-semantic-ledger.csv` · `Hermes/evidence/page-content-classification.json`

[Índice de documentación](README.md) · [Instrucciones de instalación](../../README.md) · [Revisión de fuentes y exportación](source-review.json)
