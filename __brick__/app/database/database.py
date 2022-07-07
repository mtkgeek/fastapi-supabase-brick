from app.config import Settings, get_settings
from supabase import create_client, Client


settings: Settings = get_settings()


url: str = settings.supabase_url
key: str = settings.supabase_key


supabase_client: Client = create_client(url, key)

# Use the following commands to export your supabase credentials into env variables
# export SUPABASE_URL="https://whateva.supabase.co"
# export SUPABASE_KEY="jshsdbjjdkjskslkskkklklkkkkkklkkkkkklkllkkl"
