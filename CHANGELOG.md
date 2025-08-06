# Changelog

## [Unreleased] - 2024-01-XX

### Added
- ✅ Soporte completo para imágenes en el worker-sglang
- ✅ Compatibilidad con la API de OpenAI Vision
- ✅ Soporte para imágenes via URL
- ✅ Soporte para imágenes codificadas en base64
- ✅ Soporte para contenido mixto (texto + imágenes)
- ✅ Función `process_image_content()` para procesar contenido de imágenes
- ✅ Documentación completa sobre el uso de imágenes
- ✅ Archivos de prueba para verificar el funcionamiento
- ✅ Script de prueba `test_image_support.py`

### Changed
- Modificado `handler.py` para procesar automáticamente contenido de imágenes en mensajes
- Actualizado `README.md` con ejemplos de uso de imágenes
- Mejorada la función de procesamiento de contenido para manejar casos edge

### Technical Details
- Agregadas importaciones `base64` y `json` en `handler.py`
- Implementada lógica para detectar y procesar `image_url` en mensajes
- Añadida validación para diferentes formatos de contenido
- Soporte para conversión automática de contenido de texto a formato estructurado

### Files Added
- `docs/image_support.md` - Documentación específica sobre soporte de imágenes
- `test_input_with_images.json` - Ejemplo con imagen via URL
- `test_input_with_base64_images.json` - Ejemplo con imagen base64
- `test_image_support.py` - Script de prueba completo
- `CHANGELOG.md` - Este archivo

### Files Modified
- `handler.py` - Agregado soporte para imágenes
- `README.md` - Agregada sección de ejemplos con imágenes 