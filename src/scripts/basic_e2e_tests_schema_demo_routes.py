import asyncio
import random

import aiohttp

from src.scripts.e2e_tests_helpers import rand_str, rand_enum, create_entity, get_entity, update_entity, delete_entity, \
    list_entity

BASE_URL = "http://localhost:8000"

NUM_ITEMS = 1
NUM_COMPANIES = 1
NUM_CUSTOMERS = 1
NUM_ORDERS = 1
NUM_ORDER_ITEMS = 1

# --- toggle whole-entity tests ---
is_test_companies = True
is_test_customers = True
is_test_items = True
is_test_orders = True

# --- toggle operations ---
is_create = True
is_get = True
is_update = True
is_delete = True
is_list = True

main_count = 1


# ----------------- per-entity tests -----------------

async def test_companies(client):
    print("\n== COMPANIES ==")
    base_url = f"{BASE_URL}/companies/"
    companies = []

    # create
    if is_create:
        for _ in range(NUM_COMPANIES):
            payload = {
                "name": f"Company_{rand_str(4)}",
                "username": f"user_{rand_str(4)}",
                "password": rand_str(10),
                "email": f"{rand_str(5)}@example.com",
                "location": "Tel Aviv",
                "industry": rand_enum(["Technology","Finance","Healthcare","Retail","Manufacturing"]),
                "employees": random.randint(10,100)
            }
            company = await create_entity(client, base_url, payload)
            print("Created:", company)
            companies.append(company)

    if companies and is_get:
        c = await get_entity(client, base_url, companies[0]["company_id"])
        print("Got one:", c)

    if companies and is_update:
        updated = await update_entity(client, base_url, companies[0]["company_id"], {"employees": 999})
        print("Updated:", updated)

    if companies and is_delete:
        deleted = await delete_entity(client, base_url, companies[-1]["company_id"])
        print("Deleted:", deleted)

    if is_list:
        listed = await list_entity(client, base_url)
        print("List:", listed)

    return companies

async def test_customers(client):
    print("\n== CUSTOMERS ==")
    base_url = f"{BASE_URL}/customers/"
    customers = []

    if is_create:
        for _ in range(NUM_CUSTOMERS):
            payload = {
                "username": f"cust_{rand_str(4)}",
                "password": rand_str(10),
                "email": f"{rand_str(5)}@example.com",
                "name": f"Customer {rand_str(3)}",
                "age": random.randint(18,65),
                "location": "Jerusalem"
            }
            customer = await create_entity(client, base_url, payload)
            print("Created:", customer)
            customers.append(customer)

    if customers and is_get:
        c = await get_entity(client, base_url, customers[0]["customer_id"])
        print("Got one:", c)

    if customers and is_update:
        updated = await update_entity(client, base_url, customers[0]["customer_id"], {"location": "Haifa"})
        print("Updated:", updated)

    if customers and is_delete:
        deleted = await delete_entity(client, base_url, customers[-1]["customer_id"])
        print("Deleted:", deleted)

    if is_list:
        listed = await list_entity(client, base_url)
        print("List:", listed)

    return customers

async def test_items(client, companies):
    print("\n== ITEMS ==")
    base_url = f"{BASE_URL}/items/"
    items = []

    if is_create:
        for _ in range(NUM_ITEMS):
            payload = {
                "company_id": random.choice(companies)["company_id"],
                "name": f"Item_{rand_str(4)}",
                "description": f"Description {rand_str(6)}",
                "price": round(random.uniform(1.0, 100.0), 2),
                "stock": random.randint(1,100)
            }
            item = await create_entity(client, base_url, payload)
            print("Created:", item)
            items.append(item)

    if items and is_get:
        i = await get_entity(client, base_url, items[0]["item_id"])
        print("Got one:", i)

    if items and is_update:
        updated = await update_entity(client, base_url, items[0]["item_id"], {"stock": 500})
        print("Updated:", updated)

    if items and is_delete:
        deleted = await delete_entity(client, base_url, items[-1]["item_id"])
        print("Deleted:", deleted)

    if is_list:
        listed = await list_entity(client, base_url)
        print("List:", listed)

    return items

async def test_orders(client, customers, items):
    print("\n== ORDERS ==")
    base_url = f"{BASE_URL}/orders/"
    orders = []

    if is_create:
        for _ in range(NUM_ORDERS):
            order_payload = {
                "customer_id": random.choice(customers)["customer_id"],
                "order_time": None,
                "order_items": []
            }
            for _ in range(NUM_ORDER_ITEMS):
                chosen_item = random.choice(items)
                order_item_payload = {
                    "item_id": chosen_item["item_id"],
                    "quantity": random.randint(1, 5),
                }
                order_payload['order_items'].append(order_item_payload)
            print(order_payload)
            order = await create_entity(client, base_url, order_payload)
            print("Created order:", order)
            orders.append(order)

    if orders and is_get:
        o = await get_entity(client, base_url, orders[0]["order_id"])
        print("Got one:", o)

    if orders and is_update:
        updated = await update_entity(client, base_url, orders[0]["order_id"], {"order_items": []})
        print("Updated order:", updated)

    if orders and is_delete:
        deleted = await delete_entity(client, base_url, orders[-1]["order_id"])
        print("Deleted order:", deleted)

    if is_list:
        listed = await list_entity(client, base_url)
        print("List:", listed)


    return orders


async def demo_schema_e2e_tests():
    async with aiohttp.ClientSession() as client:
        if is_test_companies:
            await test_companies(client)
        if is_test_customers:
            await test_customers(client)
        if is_test_items:
            companies = await list_entity(client, f"{BASE_URL}/companies/")
            await test_items(client, companies or [{"company_id":1}])
        if is_test_orders:
            customers = await list_entity(client, f"{BASE_URL}/customers/")
            items = await list_entity(client, f"{BASE_URL}/items/")
            await test_orders(client, customers or [{"customer_id":1}], items or [{"item_id":1,"price":10.0}])


async def main():
    for _ in range(main_count):
        asyncio.create_task(demo_schema_e2e_tests())

    await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())

