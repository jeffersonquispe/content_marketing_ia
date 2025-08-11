import boto3
import json
import os

def generar_descripcion_producto(producto_nombre, ingredientes, beneficios, num_iteraciones=3):
    """
    Genera una descripción de producto utilizando un modelo de lenguaje de Bedrock
    aplicando la técnica de auto-crítica con llamadas iterativas a la API.
    """
    try:
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=os.environ['AWS_REGION']
        )
        
        # --- PASO 1: Generar la primera descripción (llamada inicial) ---
        prompt_inicial = f"""
Human: Eres un experto en marketing de alimentos saludables. Tu objetivo es generar descripciones de producto atractivas y persuasivas.

Genera una descripción inicial para el siguiente snack.
---
Nombre del producto: {producto_nombre}
Ingredientes clave: {ingredientes}
Beneficios: {beneficios}
---
Assistant:
"""

        body = json.dumps({
            "prompt": prompt_inicial,
            "max_tokens_to_sample": 500,
            "temperature": 0.7,
        })
        
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId='anthropic.claude-v2:1',
            accept='application/json',
            contentType='application/json'
        )
        response_body = json.loads(response.get('body').read())
        ultima_descripcion = response_body.get('completion')
        
        # --- PASO 2: Bucle de mejora recursiva (llamadas iterativas) ---
        for i in range(num_iteraciones):
            criterios = [
                "Evalúa la descripción anterior en términos de autenticidad y conexión emocional.",
                "Critica la descripción por su claridad, originalidad y llamado a la acción.",
                "Mejora la descripción para que sea más persuasiva y única, enfatizando los beneficios del snack."
            ]
            criterio_actual = criterios[i % len(criterios)]
            
            # El prompt de cada iteración incluye la descripción anterior
            prompt_mejora = f"""
Human: Eres un experto en marketing de alimentos saludables.

Aquí está la descripción anterior del producto:
---
{ultima_descripcion}
---

Ahora, basándote en la descripción anterior, genera una nueva y mejorada versión. Asegúrate de abordar el siguiente criterio: "{criterio_actual}"
Assistant:
"""
            
            body_mejora = json.dumps({
                "prompt": prompt_mejora,
                "max_tokens_to_sample": 500,
                "temperature": 0.7,
            })
            
            response_mejora = bedrock_runtime.invoke_model(
                body=body_mejora,
                modelId='anthropic.claude-v2:1',
                accept='application/json',
                contentType='application/json'
            )
            response_body_mejora = json.loads(response_mejora.get('body').read())
            
            # Actualiza la descripción con la última versión mejorada
            ultima_descripcion = response_body_mejora.get('completion')
            
        return ultima_descripcion

    except Exception as e:
        return f"Error al generar la descripción: {e}"

def generar_imagen_promocional(prompt_imagen):
    """
    Genera una imagen promocional utilizando un modelo de difusión de Bedrock.
    """
    try:
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=os.environ['AWS_REGION']
        )
        prompt = f'''
        Generate a high-quality, professional marketing image for a healthy snack.
        The image should be visually appealing and focus on the prompt:
        '{prompt_imagen}'
        '''
        body = json.dumps({
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 10,
            "seed": 0,
            "steps": 50,
        })
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId='stability.stable-diffusion-xl-v1',
            accept='application/json',
            contentType='application/json'
        )
        response_body = json.loads(response.get('body').read())
        image_base64 = response_body.get('artifacts')[0].get('base64')
        return f"data:image/png;base64,{image_base64}"
    except Exception as e:
        return f"Error al generar la imagen: {e}"

def generar_resumen_comentarios(comentarios):
    """
    Genera un resumen de comentarios de clientes utilizando un modelo de lenguaje de Bedrock.
    """
    try:
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=os.environ['AWS_REGION']
        )
        
        # Formato de prompt correcto para el modelo de Bedrock
        prompt = f"""
Human: Actúa como un analista de mercado experto en productos de consumo masivo. Lee los siguientes comentarios de clientes sobre un nuevo snack y genera un resumen conciso que destaque las opiniones clave, tanto positivas como negativas.
--- Comentarios ---
{comentarios}
---
Resumen:
Assistant:
"""

        body = json.dumps({
            "prompt": prompt,
            "max_tokens_to_sample": 500,
            "temperature": 0.5,
        })

        response = bedrock_runtime.invoke_model(
            body=body,
            modelId='anthropic.claude-v2',
            accept='application/json',
            contentType='application/json'
        )

        response_body = json.loads(response.get('body').read())
        return response_body.get('completion')

    except Exception as e:
        return f"Error al generar el resumen: {e}"