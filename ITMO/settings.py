from dotenv import load_dotenv
import os 

load_dotenv()

CREDENTIAL = os.getenv("credential", "")
