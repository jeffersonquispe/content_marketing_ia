import boto3
import os
import decimal 
import json

class DynamoDBManager:
    def __init__(self, table_name='ProductComments'):
        self.dynamodb = boto3.resource('dynamodb', region_name=os.environ['AWS_REGION'])
        self.table = self.dynamodb.Table(table_name)
        print(f"✅ Conectado a la tabla DynamoDB: {table_name}")

    def create_table(self):
        """
        Crea la tabla DynamoDB si no existe.
        Ideal para configuración inicial.
        """
        try:
            self.dynamodb.create_table(
                TableName=self.table.name,
                KeySchema=[
                    {
                        'AttributeName': 'comment_id',
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'comment_id',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'timestamp',
                        'AttributeType': 'S' # Se puede usar 'N' para números si el formato es EPOCH
                    },
                    {
                        'AttributeName': 'sentiment',
                        'AttributeType': 'S'
                    }
                ],
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'SentimentTimestampIndex',
                        'KeySchema': [
                            {
                                'AttributeName': 'sentiment',
                                'KeyType': 'HASH'
                            },
                            {
                                'AttributeName': 'timestamp',
                                'KeyType': 'RANGE'
                            }
                        ],
                        'Projection': {
                            'ProjectionType': 'ALL'
                        },
                        'ProvisionedThroughput': {
                            'ReadCapacityUnits': 5,
                            'WriteCapacityUnits': 5
                        }
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            self.table.wait_until_exists()
            print(f"✅ Tabla '{self.table.name}' creada exitosamente.")
        except self.dynamodb.meta.client.exceptions.ResourceInUseException:
            print(f"✅ Tabla '{self.table.name}' ya existe.")
        except Exception as e:
            print(f"❌ Error al crear tabla DynamoDB: {e}")


    def add_comment(self, comment_data):
        """
        Añade un nuevo comentario procesado a la tabla DynamoDB.
        """
        try:
            # Convertir floats a Decimal para DynamoDB (buena práctica para números exactos)
            item = json.loads(json.dumps(comment_data), parse_float=decimal.Decimal)
            self.table.put_item(Item=item)
            # print(f" Comentario '{comment_data['comment_id']}' añadido a DynamoDB.")
            return True
        except Exception as e:
            print(f"❌ Error al añadir comentario a DynamoDB: {e}")
            return False

    def get_all_comments(self):
        """
        Obtiene todos los comentarios de la tabla DynamoDB.
        """
        try:
            response = self.table.scan()
            data = response['Items']
            while 'LastEvaluatedKey' in response:
                response = self.table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                data.extend(response['Items'])
            
            # Convertir Decimal de vuelta a float si es necesario para el dashboard
            for item in data:
                for key, value in item.items():
                    if isinstance(value, decimal.Decimal):
                        item[key] = float(value)
            return data
        except Exception as e:
            print(f" Error al obtener comentarios de DynamoDB: {e}")
            return []
    
    def get_latest_comments(self, limit=10):
        """
        Obtiene los N comentarios más recientes de DynamoDB.
        Requiere ordenar por timestamp después de la consulta.
        """
        try:
            response = self.table.scan() # Scan para prototipo, en producción usar Query con GSI si es muy grande
            comments = sorted(response['Items'], key=lambda x: x['timestamp'], reverse=True)
            # Convertir Decimal a float para el dashboard
            for item in comments:
                for key, value in item.items():
                    if isinstance(value, decimal.Decimal):
                        item[key] = float(value)
            return comments[:limit]
        except Exception as e:
            print(f" Error al obtener últimos comentarios de DynamoDB: {e}")
            return []