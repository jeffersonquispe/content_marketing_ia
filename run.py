import subprocess
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

# Inicia la aplicación Streamlit directamente
import os
print(f"AWS_REGION: {os.getenv('AWS_REGION')}")
subprocess.run(["streamlit", "run", "src/app/app.py"])