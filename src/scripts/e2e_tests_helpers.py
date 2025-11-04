import random
import string
from os import getenv
from dotenv import load_dotenv

AUTH_TOKEN = "super_secret_token"
BASE_URL = "http://localhost:8000"

load_dotenv()

admin_token = getenv("ADMIN_TOKEN")

HEADERS = {
    "authorization": f"Bearer {admin_token}",
    "dal_auth_token": AUTH_TOKEN,
    "Content-Type": "application/json"
}

def rand_str(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def rand_enum(enum_list):
    return random.choice(enum_list)

async def safe_request(method, client, url, **kwargs):
    """Wrap aiohttp requests with error handling; stop on error."""
    try:
        async with client.request(method, url, headers=HEADERS, **kwargs) as resp:
            if resp.status >= 400:
                text = await resp.text()
                raise RuntimeError(f"HTTP {resp.status} at {url}: {text}")
            return await resp.json()
    except Exception as e:
        print("Error during request:", e)
        raise

async def create_entity(client, url, payload):
    return await safe_request("POST", client, url, json=payload)

async def get_entity(client, url, entity_id):
    return await safe_request("GET", client, f"{url}{entity_id}")

async def list_entity(client, url):
    return await safe_request("GET", client, url)

async def update_entity(client, url, entity_id, payload):
    return await safe_request("PUT", client, f"{url}{entity_id}", json=payload)

async def delete_entity(client, url, entity_id):
    return await safe_request("DELETE", client, f"{url}{entity_id}")