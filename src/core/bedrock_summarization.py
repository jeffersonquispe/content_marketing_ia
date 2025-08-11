import boto3
import json
import os

def generate_summary_bedrock(comments_text_list):
    """
    Genera un resumen conciso de una lista de comentarios usando Amazon Bedrock (Anthropic Claude).
    """
    bedrock_runtime = boto3.client(
        service_name='bedrock-runtime',
        region_name=os.environ['AWS_REGION']
    )
    
    comments_str = "\n".join(comments_text_list)
    
    prompt = f"""
Human: Actúa como un analista de mercado experto. Lee los siguientes comentarios de clientes sobre un nuevo snack y genera un resumen conciso que destaque las opiniones clave, tanto positivas como negativas, y temas recurrentes.

--- Comentarios ---
{comments_str}
---

Resumen:
Assistant:
"""
    
    try:
        body = json.dumps({
            "prompt": prompt,
            "max_tokens_to_sample": 500,
            "temperature": 0.5,
            "top_p": 0.9,
        })
        
        response = bedrock_runtime.invoke_model(
            body=body,
            modelId='anthropic.claude-v2', # Asegúrate de que este modelo esté habilitado en tu cuenta Bedrock
            accept='application/json',
            contentType='application/json'
        )
        
        response_body = json.loads(response.get('body').read())
        return response_body.get('completion', "No se pudo generar el resumen.")
    
    except Exception as e:
        print(f"❌ Error al generar resumen con Bedrock: {e}")
        return f"Error al generar el resumen: {e}"