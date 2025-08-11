import boto3
import json
import os
import datetime

def upload_comments_to_s3(comments_data, bucket_name, file_prefix='comments/'):
    """
    Simula la carga de comentarios (JSON) a S3.
    En un entorno real, los comentarios llegarían de forma continua.
    """
    s3_client = boto3.client('s3', region_name=os.environ['AWS_REGION'])
    
    # Crea un timestamp para el nombre del archivo, simulando una carga en tiempo real
    timestamp_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_key = f"{file_prefix}comments_{timestamp_str}.json"
    
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=json.dumps(comments_data, ensure_ascii=False).encode('utf-8'),
            ContentType='application/json'
        )
        print(f"✅ Archivo '{file_key}' cargado a S3 exitosamente.")
        return True
    except Exception as e:
        print(f"❌ Error al cargar a S3: {e}")
        return False

def get_comment_from_s3(bucket_name, file_key):
    """
    Obtiene un archivo JSON de comentarios desde S3.
    (Usado por Lambda o para pruebas directas)
    """
    s3_client = boto3.client('s3', region_name=os.environ['AWS_REGION'])
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        file_content = response['Body'].read().decode('utf-8')
        return json.loads(file_content)
    except Exception as e:
        print(f"❌ Error al obtener archivo de S3: {e}")
        return None