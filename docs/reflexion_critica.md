# Reflexión Crítica: Limitaciones de la IA en este Sistema

## 1. Alucinaciones y errores

Los modelos de lenguaje pueden generar información incorrecta con total confianza. En este sistema, esto se traduce en:

- Pasos de resolución inventados que no corresponden al manual real
- Clasificaciones erróneas de urgencia (infravalorar una incidencia crítica)
- Correos con instrucciones técnicas incorrectas enviados al usuario

**Mitigación aplicada:** El sistema RAG ancla las respuestas al contenido del manual. Aun así, la supervisión humana antes de enviar cualquier respuesta es imprescindible.

## 2. Importancia del prompt

La calidad del resultado depende directamente del diseño del prompt. Un prompt mal diseñado puede producir:

- JSON mal formateado que rompe la aplicación
- Respuestas genéricas sin usar el contexto del manual
- Cambios de idioma o formato inesperados

**Mitigación aplicada:** El prompt incluye instrucciones explícitas de formato, ejemplos de salida esperada, y restricciones claras.

## 3. Sesgos del modelo

El modelo puede mostrar sesgos derivados de sus datos de entrenamiento:

- Priorizar soluciones para hardware o software más común en entornos anglosajones
- Subestimar la urgencia de incidencias descritas con lenguaje informal
- Generar correos con un tono cultural no adaptado al contexto local

## 4. Privacidad y datos sensibles

Las incidencias técnicas pueden contener información sensible:

- Nombres de usuarios, correos electrónicos
- Nombres de sistemas internos o contraseñas mencionadas por error
- Datos de configuración de red

**Consideración:** Los datos se envían a la API de AWS Bedrock. Es necesario revisar la política de privacidad y datos de AWS y asegurarse de anonimizar cualquier dato personal antes de enviarlo al modelo.

## 5. Necesidad de supervisión humana

Este sistema es una **herramienta de apoyo**, no un sustituto del técnico. La IA:

- No puede verificar físicamente el estado del hardware
- No tiene acceso a los sistemas internos en tiempo real
- Puede equivocarse en incidencias poco comunes o no documentadas en el manual

**Conclusión:** El técnico debe revisar siempre la hoja de ruta y el correo generado antes de actuar o enviarlo. La IA reduce el tiempo de gestión, pero la decisión final es humana.
