import json
import os
import sys
from dotenv import load_dotenv
# Carga las variables del archivo .env
load_dotenv()

# Add the 'src' directory to Python's path to ensure imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Now we can import the function directly
from core.data_ingestion import upload_comments_to_s3

# Define the bucket name
bucket_name = 'bucket-comentarios-snacks'

# Load data from the JSON file
with open('comments_data.json', 'r', encoding='utf-8') as f:
    comments = json.load(f)

# Upload the data to the S3 bucket
upload_comments_to_s3(comments, bucket_name)