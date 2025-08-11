import boto3
import os

def analyze_sentiment(text):
    """
    Analiza el sentimiento de un texto usando Amazon Comprehend.
    Retorna 'POSITIVE', 'NEGATIVE', 'NEUTRAL', 'MIXED' y su puntaje.
    """
    comprehend = boto3.client('comprehend', region_name=os.environ['AWS_REGION'])
    try:
        response = comprehend.detect_sentiment(Text=text, LanguageCode='es')
        sentiment = response['Sentiment']
        sentiment_score = response['SentimentScore'] # Diccionario con puntajes
        return sentiment, sentiment_score
    except Exception as e:
        print(f"❌ Error al analizar sentimiento con Comprehend: {e}")
        return "UNKNOWN", {}

def extract_entities(text):
    """
    Extrae entidades clave de un texto usando Amazon Comprehend.
    Retorna una lista de entidades y sus tipos (ej. PRODUCT, LOCATION, ORGANIZATION).
    """
    comprehend = boto3.client('comprehend', region_name=os.environ['AWS_REGION'])
    try:
        response = comprehend.detect_entities(Text=text, LanguageCode='es')
        entities = [{'Text': entity['Text'], 'Type': entity['Type'], 'Score': entity['Score']} 
                    for entity in response['Entities']]
        return entities
    except Exception as e:
        print(f"❌ Error al extraer entidades con Comprehend: {e}")
        return []