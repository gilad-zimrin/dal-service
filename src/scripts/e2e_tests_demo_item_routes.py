import asyncio
import random
import string

import httpx

from src.models.item import ItemCreate

BASE_URL = "http://localhost:8000/items"
AUTH_TOKEN = "super_secret_token"
NUM_ITEMS = 2
main_count = 1

HEADERS = {
    "Authorization": AUTH_TOKEN,
    "Content-Type": "application/json"
}


def random_string(length=8):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_mock_item():
    return {
        "name": f"Item {random_string(5)}",
        "description": f"Description {random_string(10)}",
        "price": round(random.uniform(1.0, 100.0), 2)
    }


async def work():
    async with httpx.AsyncClient() as client:
        created_items = []

        # --- CREATE items ---
        print("Creating items...")
        for _ in range(NUM_ITEMS):
            mock_data = generate_mock_item()

            payload = dict(ItemCreate(**mock_data))
            print(payload)
            r = await client.post(BASE_URL + "/", json=payload, headers=HEADERS)
            if r.status_code == 200 or r.status_code == 201:
                item = r.json()
                created_items.append(item)
                print("Created:", item)
            else:
                print("Failed to create:", r.status_code, r.text)

        # --- LIST all items ---
        print("\nListing all items...")
        r = await client.get(BASE_URL + "/", headers=HEADERS)
        print(r.json())

        # --- GET each item by ID ---
        print("\nGetting each item by ID...")
        existing_items = []
        for item in created_items:
            r = await client.get(f"{BASE_URL}/{item['id']}", headers=HEADERS)
            print(r.json())
            existing_items.append(r.json())

        # --- UPDATE each item ---
        print("\nUpdating items...")
        for item in existing_items:
            update_payload = {
                "name": item["name"] + "_updated",
                "price": item["price"] + 1
            }
            r = await client.put(f"{BASE_URL}/{item['item_id']}", json=update_payload, headers=HEADERS)
            print("Updated:", r.json())

        # --- DELETE each item ---
        print("\nDeleting items...")
        for item in created_items:
            r = await client.delete(f"{BASE_URL}/{item['id']}", headers=HEADERS)
            print(f"Deleted {item['id']}:", r.json())


async def main():
    for _ in range(main_count):
        asyncio.create_task(work())

    await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())

