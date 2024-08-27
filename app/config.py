import os
from pathlib import Path

from dotenv import load_dotenv


dotenv_path = Path(__file__).resolve().parent / '..' / '.env'

load_dotenv(dotenv_path)

# "environ" access and manipulate environment variables
sttgs = os.environ
