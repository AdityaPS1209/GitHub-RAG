from motor.motor_asyncio import AsyncIOMotorClient
from backend.core.config import settings
import urllib.parse
import certifi

class Database:
    client: AsyncIOMotorClient = None

db = Database()

def connect_to_mongo():
    connection_url = settings.MONGODB_URL
    
    # If the URL contains credentials, we need to ensure they are properly URL-encoded
    if "@" in connection_url and "://" in connection_url:
        try:
            scheme, rest = connection_url.split("://", 1)
            # Use rsplit to separate at the LAST '@' marker in case the password contains '@'
            credentials, host_info = rest.rsplit("@", 1)
            if ":" in credentials:
                username, password = credentials.split(":", 1)
                # Ensure we don't double-quote if it was already quoted
                username = urllib.parse.unquote(username)
                password = urllib.parse.unquote(password)
                # Quote the username and password
                encoded_user = urllib.parse.quote_plus(username)
                encoded_pass = urllib.parse.quote_plus(password)
                connection_url = f"{scheme}://{encoded_user}:{encoded_pass}@{host_info}"
        except Exception:
            # If parsing fails, fall back to the original URL and let motor handle it
            pass

    # Use certifi to provide the CA bundle for TLS verification
    db.client = AsyncIOMotorClient(connection_url, tlsCAFile=certifi.where())
    print(f"Connected to MongoDB")

def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Closed MongoDB connection")

def get_database():
    return db.client[settings.MONGODB_DB_NAME]
