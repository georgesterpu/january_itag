from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SERVICE_FQDN_SUPABASEKONG"),
    os.getenv("SERVICE_SUPABASEANON_KEY")
)
