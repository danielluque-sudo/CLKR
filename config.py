# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Supabase credentials
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Anthropic API
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# Scraper settings
SCRAPER_DELAY = 2  # Seconds between requests
MAX_RETRIES = 3
TIMEOUT = 30
TEST_MODE = os.getenv('TEST_MODE', 'false').lower() == 'true'

# File paths
DATA_DIR = 'data'
SAMPLE_OUTPUT_DIR = 'data/sample_output'
LOGS_DIR = 'logs'

# Subject area classification keywords
SUBJECT_AREAS = {
    'laboral': ['trabajo', 'empleado', 'salario', 'prestaciones', 'seguridad social', 'pensión'],
    'tributario': ['impuesto', 'tributo', 'DIAN', 'renta', 'IVA', 'fiscal', 'tributario'],
    'civil': ['contrato', 'obligaciones', 'derechos civiles', 'persona natural', 'código civil'],
    'penal': ['delito', 'pena', 'prisión', 'código penal', 'delincuencia'],
    'comercial': ['sociedad', 'comerciante', 'registro mercantil', 'empresa', 'comercio'],
    'administrativo': ['función pública', 'entidad estatal', 'procedimiento administrativo'],
    'inmigración': ['visa', 'extranjero', 'migración', 'residencia', 'cédula de extranjería'],
    'ambiental': ['medio ambiente', 'recursos naturales', 'contaminación', 'sostenibilidad'],
    'educación': ['educación', 'universidad', 'colegio', 'ministerio de educación'],
    'salud': ['salud', 'EPS', 'sistema de salud', 'medicina', 'hospital']
}
