# Soporte de Imágenes en worker-sglang

Este documento describe cómo usar el soporte de imágenes en el worker-sglang de RunPod.

## Características

- ✅ Soporte para imágenes via URL
- ✅ Soporte para imágenes codificadas en base64
- ✅ Compatible con la API de OpenAI Vision
- ✅ Soporte para contenido mixto (texto + imágenes)
- ✅ Streaming y no-streaming

## Formato de Entrada

El worker acepta imágenes en el mismo formato que la API de OpenAI Vision:

### Imágenes via URL

```json
{
  "input": {
    "openai_route": "/v1/chat/completions",
    "openai_input": {
      "model": "your-model-name",
      "messages": [
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "What's in this image?"},
            {
              "type": "image_url",
              "image_url": {
                "url": "https://example.com/image.jpg"
              }
            }
          ]
        }
      ]
    }
  }
}
```

### Imágenes codificadas en base64

```json
{
  "input": {
    "openai_route": "/v1/chat/completions",
    "openai_input": {
      "model": "your-model-name",
      "messages": [
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "Describe this image:"},
            {
              "type": "image_url",
              "image_url": {
                "url": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD..."
              }
            }
          ]
        }
      ]
    }
  }
}
```

## Ejemplos de Uso

### Python con OpenAI SDK

```python
from openai import OpenAI
import base64

# Inicializar el cliente
client = OpenAI(
    api_key="your-runpod-api-key",
    base_url="https://api.runpod.ai/v2/<ENDPOINT_ID>/openai/v1"
)

# Ejemplo con URL de imagen
response = client.chat.completions.create(
    model="your-model-name",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"
                }
            }
        ]
    }],
    max_tokens=100
)

print(response.choices[0].message.content)
```

### Python con base64

```python
import base64

# Leer y codificar la imagen
with open("image.jpg", "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

response = client.chat.completions.create(
    model="your-model-name",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this image:"},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{encoded_image}"
                }
            }
        ]
    }],
    max_tokens=100
)
```

## Contenido Mixto

Puedes combinar texto e imágenes en el mismo mensaje:

```python
response = client.chat.completions.create(
    model="your-model-name",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Please analyze this image and tell me:"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://example.com/image.jpg"
                }
            },
            {"type": "text", "text": "1. What objects do you see? 2. What colors are prominent?"}
        ]
    }],
    max_tokens=150
)
```

## Formatos de Imagen Soportados

- JPEG (.jpg, .jpeg)
- PNG (.png)
- GIF (.gif)
- WebP (.webp)

## Limitaciones

1. **Tamaño de imagen**: Las imágenes deben ser razonablemente pequeñas para evitar problemas de memoria
2. **Modelo**: El modelo debe tener soporte para visión (vision capabilities)
3. **URLs**: Las URLs deben ser accesibles públicamente
4. **Base64**: Las imágenes codificadas en base64 deben incluir el prefijo `data:image/...;base64,`

## Solución de Problemas

### Error: "Model does not support vision"

Asegúrate de que el modelo que estás usando tenga capacidades de visión. No todos los modelos de SGLang soportan imágenes.

### Error: "Invalid image format"

Verifica que:
- La URL de la imagen sea válida y accesible
- El formato de imagen sea soportado
- La codificación base64 sea correcta

### Error: "Image too large"

Reduce el tamaño de la imagen antes de enviarla.

## Archivos de Prueba

- `test_input_with_images.json`: Ejemplo con imagen via URL
- `test_input_with_base64_images.json`: Ejemplo con imagen base64
- `test_image_support.py`: Script de prueba completo 