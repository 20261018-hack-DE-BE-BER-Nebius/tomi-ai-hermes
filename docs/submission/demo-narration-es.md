---
id: demo-narration-es
topic: demo-narration
lang: es
title: "Narración Tomi: entrega de tres minutos y entrevista ampliada"
type: guide
status: evidence-draft
updated: "2026-10-18"
tags: [tomi, submission, evidence, es]
---

[EN](demo-narration-en.md) · [ES](demo-narration-es.md) · [DE](demo-narration-de.md) · [FR](demo-narration-fr.md)

> Estado de los vídeos: ambos archivos finales están incluidos en este repositorio y verificados localmente (entrega: 180.000 segundos; recorrido: 279.722656 segundos). La revisión visual y técnica independiente fue satisfactoria; no se certificaron escucha, inteligibilidad ni pronunciación. No se ha realizado la entrega en el portal. La transcripción automática del MOV terminó (46 fragmentos, 87 segmentos), pero faltan escucha y revisión de fidelidad.

# Tomi

## Narración de entrega de tres minutos

Tomi conecta la Encyclopaedia Britannica histórica con Wikipedia y muestra qué sostiene cada comparación.

Seleccionamos cien páginas de forma reproducible y comprobamos cada hash de imagen. Todas recibieron llamadas reales Nemotron Parse. Se aceptaron noventa y ocho respuestas completas, incluidas tres hojas en blanco; una lámina astronómica sigue parcial y una cubierta no contiene prosa útil. OCR aceptado no significa transcripción perfecta.

Los cuatro modelos NVIDIA exigidos ya funcionan. Embed y Rerank utilizan la GPU Nebius asignada. LanceDB almacena y busca vectores. Nemotron Super VL opera nuestra herramienta de evidencias Hermes mediante el gateway Rust.

Mostramos tres resultados acotados y respaldados. Las piezas históricas son de madera, mientras el texto moderno define un astillero. Ambas fuentes asocian el litro con un decímetro cúbico. El ejemplo de blanqueo contrasta recipientes y gas históricos con el objetivo moderno de eliminar color.

Las primeras versiones amplias fallaron. La búsqueda devolvió empresas navales, las políticas de medición desplazaron las definiciones y el OCR del blanqueo no sostuvo una comparación completa del proceso. Conservamos esos fallos junto a las preguntas acotadas exitosas.

Hermes solo selecciona fragmentos ofrecidos. El servidor los vincula a citas y posiciones Unicode exactas. Las citas inválidas fallan la validación. Una cita válida aún exige revisar el soporte documental; no convierte automáticamente una afirmación en verdad.

Las 100 páginas originales están contabilizadas. La recuperación semántica real terminó para 96 páginas con texto o parciales:23 resultados candidatos y 73 ambiguos. Tres hojas en blanco y una cubierta sin texto quedan sin asociación; la lámina astronómica parcial está entre las 96. Se conservan fallos originales y reintentos selectivos. Estos recuentos no miden exactitud de asociación.

El archivo compilado contiene cien documentos en 187 páginas PDF. La aplicación multilingüe muestra fuentes y herramientas; pruebas públicas verificaron streaming, redirección, cancelación y eventos guardados.

Tomi permite inspeccionar respuestas útiles y conserva las razones de los fallos.

## Narración ampliada para entrevista

Tomi permite comparar la Encyclopaedia Britannica histórica con Wikipedia. Su propósito es hacer inspeccionables las evidencias y la incertidumbre, sin considerar una respuesta fluida como prueba suficiente.

Seleccionamos cien páginas mediante un manifiesto reproducible y comprobamos los hashes. Cada imagen recibió una llamada real Nemotron Parse 3.5. Se aceptaron noventa y ocho respuestas completas sin truncamiento, incluidas tres hojas en blanco con solo controles de diseño. Una lámina astronómica necesitó recortes y sigue parcial. Una cubierta no tiene prosa útil. Conservamos cien identidades y todos los intentos fallidos. Son resultados de extracción, no exactitud OCR certificada.

La ruta exigida ya utiliza los cuatro modelos NVIDIA. Los candidatos proceden de la instantánea Wikimedia fijada, con texto completo, revisión y hashes comprobados. Embed representa contenido; LanceDB almacena y busca vectores; Rerank puntúa relevancia. Ambos modelos de recuperación funcionan en la GPU Nebius asignada. Super VL dirige la herramienta real Hermes mediante nuestro gateway Rust. Las credenciales permanecen en core.

Tres comparaciones acotadas superaron una revisión del asistente contra sus fuentes. El caso naval contrasta piezas históricas de madera con la definición moderna de astillero. El de medición encuentra el litro asociado al decímetro cúbico en ambos textos. Su prosa normaliza la tipografía del símbolo cúbico, pero las citas permanecen exactas. El de blanqueo compara recipientes y gas históricos con el objetivo moderno de eliminar color. Son observaciones limitadas, no afirmaciones amplias de progreso científico.

Las versiones amplias anteriores fallaron. La búsqueda naval favoreció empresas; los candidatos de medición trataban políticas en lugar de definiciones; el OCR del blanqueo no sostuvo una comparación completa de técnicas. Conservamos esos fallos y las preguntas posteriores, con temas de búsqueda explícitos y trazas de modelos. No se declara certificación humana independiente.

También reprodujimos errores al copiar citas. La herramienta reparada ofrece identificadores inmutables de fragmentos. Super VL selecciona esos identificadores; el servidor recupera citas y posiciones Unicode exactas y aplica el mismo validador estricto. Se rechazan identificadores desconocidos, modificaciones y referencias de un solo corpus. Una cita válida todavía necesita revisión de soporte. Conservamos la pregunta original separada de la búsqueda para no perder el alcance solicitado.

Las 100 páginas originales están contabilizadas. La recuperación semántica real terminó para 96 páginas con texto o parciales:23 resultados candidatos y 73 ambiguos. Tres hojas en blanco y una cubierta sin texto quedan sin asociación; la lámina astronómica parcial está entre las 96. Se conservan fallos originales y reintentos selectivos. Estos recuentos no miden exactitud de asociación. Los logits de relevancia no son probabilidades de verdad; no tenemos exactitud medida contra un conjunto etiquetado. Vocabulario y frecuencias normalizadas describen textos, con límites por OCR y cobertura desigual.

El archivo tiene PDF compilado para cien documentos, 187 páginas, LaTeX editable y visor estático. La aplicación admite cuatro idiomas. Pruebas públicas verificaron streaming, redirección, cancelación, eventos guardados y cierre de sesión. Se probaron generación de imagen y emisión de sesión realtime; no micrófono físico ni reproducción.

Seis servicios se ejecutan en Azure; solo la web es pública. Azure Blob nativo permite escrituras LanceDB. Quedan límites como el rol administrativo de base de datos y la fiabilidad de preguntas amplias. Entregamos un flujo inspeccionable con éxitos y fallos, sin prometer asociar toda fuente ni responder cualquier pregunta.

## Límites de producción y evidencias

El PDF exige tres minutos. Los vídeos finales incluidos miden 180.000 y 279.722656 segundos y tienen hashes coincidentes y recibos de decodificación completa. El guion inglés ampliado de preparación sigue por debajo de600palabras. Los cuatro modelos exigidos tienen ejecuciones reales; la comparación Nemotron pública terminó con siete fuentes y aviso de revisión. La asociación completa terminó con ambigüedad explícita. El asistente revisó los seis casos; falta certificación humana independiente. No se afirma entrega en portal, premio ni fidelidad de audio físico.

[submission-guide-es](submission-guide-es.md) · [interview-preparation-es](interview-preparation-es.md)

`Hermes/evidence/reviewed-six-cases.json` · `Hermes/evidence/live-nemotron-matching-20261018T1742Z/progress.json` · `Hermes/archive/assets/compile-receipt.json`

Clasificación semántica final:95 páginas con texto Parse,1 lámina astronómica parcial(fila2243),3 hojas en blanco(filas374,1615,2077) y1 cubierta sin texto(fila452)=100 originales. Se inspeccionaron visualmente las tres hojas. Las98 respuestas Parse completas aceptadas incluyen esas3 hojas con solo controles; aceptación no equivale a prosa útil ni exactitud OCR. Se conservan recibos. `Hermes/evidence/page-content-classification.json` contiene100 identidades y hashes.


Las 100 páginas originales están contabilizadas. La recuperación semántica real terminó para 96 páginas con texto o parciales:23 resultados candidatos y 73 ambiguos. Tres hojas en blanco y una cubierta sin texto quedan sin asociación; la lámina astronómica parcial está entre las 96. Se conservan fallos originales y reintentos selectivos. Estos recuentos no miden exactitud de asociación.

`Hermes/evidence/100-page-semantic-summary.json` · `Hermes/evidence/100-page-semantic-ledger.csv` · `Hermes/evidence/page-content-classification.json`

[Índice de documentación](README.md) · [Instrucciones de instalación](../../README.md) · [Revisión de fuentes y exportación](source-review.json)
