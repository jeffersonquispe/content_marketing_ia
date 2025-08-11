import json
import os
import datetime
from .data_ingestion import get_comment_from_s3
from .sentiment_analysis import analyze_sentiment, extract_entities
from .bedrock_summarization import generate_summary_bedrock # Para resúmenes por lotes
from .database_management import DynamoDBManager

def lambda_handler(event, context):
    """
    Función principal de AWS Lambda para procesar comentarios.
    Se activa con un evento de S3.
    """
    s3_bucket = event['Records'][0]['s3']['bucket']['name']
    s3_key = event['Records'][0]['s3']['object']['key']

    print(f"⚡ Nuevo archivo S3 detectado: {s3_key} en bucket {s3_bucket}")

    # 1. Obtener los comentarios del archivo S3
    comments_raw = get_comment_from_s3(s3_bucket, s3_key)
    if not comments_raw:
        print("🔴 No se pudieron obtener comentarios del archivo S3.")
        return {'statusCode': 500, 'body': json.dumps('Error al procesar el archivo S3')}

    db_manager = DynamoDBManager()
    processed_comments = []
    all_comment_texts = [] 

    for comment in comments_raw:
        comment_id = comment.get('id')
        comment_text = comment.get('text')
        timestamp = comment.get('timestamp')

        if not all([comment_id, comment_text, timestamp]):
            print(f"🟡 Comentario inválido, saltando: {comment}")
            continue

        # 2. Análisis de Sentimiento y Extracción de Entidades
        sentiment, sentiment_score = analyze_sentiment(comment_text)
        entities = extract_entities(comment_text)
        
        all_comment_texts.append(comment_text) # Añadir para posible resumen de lotes

        # 3. Preparar datos para DynamoDB
        processed_comment_data = {
            'comment_id': comment_id,
            'timestamp': timestamp,
            'text': comment_text,
            'sentiment': sentiment,
            'sentiment_score': sentiment_score, # Guardar el diccionario completo
            'entities': entities
        }
        
        # 4. Almacenar en DynamoDB
        if db_manager.add_comment(processed_comment_data):
            processed_comments.append(processed_comment_data)
        else:
            print(f"❌ Fallo al añadir comentario {comment_id} a DynamoDB.")

    # 5.  Generar un resumen de Bedrock para el lote de comentarios recién procesados
    if all_comment_texts:
        summary = generate_summary_bedrock(all_comment_texts)
        print(f"✨ Resumen de Bedrock para este lote de comentarios: {summary[:200]}...") # Imprime los primeros 200 chars

    print(f"✅ Procesamiento completado para {len(processed_comments)} comentarios.")
    return {
        'statusCode': 200,
        'body': json.dumps(f'Procesados {len(processed_comments)} comentarios.')
    }