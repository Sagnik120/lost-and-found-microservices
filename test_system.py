import requests
import time


# CONFIG (CHANGE IP IF NEEDED)


AUTH_BASE = "http://<VM2_IP>:8000"
ITEM_BASE = "http://<VM2_IP>:8001"

# Example:
# AUTH_BASE = "http://192.168.56.102:8000"
# ITEM_BASE = "http://192.168.56.102:8001"


def log(title):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)



# 1. REGISTER USERS


log("REGISTER USERS")

u1 = {
    "name": "User One",
    "email": "user1@test.com",
    "password": "test123"
}

u2 = {
    "name": "User Two",
    "email": "user2@test.com",
    "password": "test123"
}

print(requests.post(f"{AUTH_BASE}/register", json=u1).json())
print(requests.post(f"{AUTH_BASE}/register", json=u2).json())

time.sleep(1)



# 2. LOGIN USERS


log("LOGIN USERS")

login1 = requests.post(f"{AUTH_BASE}/login", json={
    "email": u1["email"],
    "password": u1["password"]
}).json()

login2 = requests.post(f"{AUTH_BASE}/login", json={
    "email": u2["email"],
    "password": u2["password"]
}).json()

print("User1:", login1)
print("User2:", login2)

user1_id = login1["user_id"]
user2_id = login2["user_id"]

time.sleep(1)



# 3. REPORT LOST ITEM (USER1)


log("USER1 REPORTS LOST ITEM")

lost_item = {
    "item_name": "Wallet",
    "description": "Black leather wallet",
    "location": "Library",
    "user_id": user1_id
}

print(requests.post(f"{ITEM_BASE}/lost-item", json=lost_item).json())

time.sleep(1)



# 4. REPORT FOUND ITEM (USER2)


log("USER2 REPORTS FOUND ITEM")

found_item = {
    "item_name": "Wallet",
    "description": "Found near desk",
    "location": "Library",
    "user_id": user2_id
}

print(requests.post(f"{ITEM_BASE}/found-item", json=found_item).json())

time.sleep(1)



# 5. VERIFY MATCHING


log("VERIFY MATCHED ITEMS")

items = requests.get(f"{ITEM_BASE}/items").json()

for item in items:
    print(item)

matched_items = [i for i in items if i["status"] == "MATCHED"]
assert len(matched_items) >= 1, "Matching failed!"

matched_item_id = matched_items[0]["id"]


# 6. MARK AS RETURNED (USER1)


log("MARK ITEM AS RETURNED")

res = requests.put(
    f"{ITEM_BASE}/items/{matched_item_id}/returned/{user1_id}"
).json()

print(res)


# 7. FINAL VERIFICATION


log("FINAL STATE")

final_items = requests.get(f"{ITEM_BASE}/items").json()
for item in final_items:
    print(item)

print("\n SYSTEM TEST COMPLETED SUCCESSFULLY")
