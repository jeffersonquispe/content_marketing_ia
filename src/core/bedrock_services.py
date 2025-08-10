import boto3
import json
import os

def generar_descripcion_producto(producto_nombre, ingredientes, beneficios):
    """
    Genera una descripción de producto utilizando un modelo de lenguaje de Bedrock.
    """
    try:
        bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=os.environ['AWS_REGION']
        )
        
        # Formato de prompt correcto para el modelo de Bedrock
        prompt = f"""
Human: Eres un experto en marketing de alimentos saludables.
Genera una descripción de producto atractiva y persuasiva para el siguiente snack.
---
Nombre del producto: {producto_nombre}
Ingredientes clave: {ingredientes}
Beneficios: {beneficios}
---
Descripción:
Assistant:
"""

        body = json.dumps({
            "prompt": prompt,
            "max_tokens_to_sample": 200,
            "temperature": 0.7,
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