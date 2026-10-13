from schemas import UserCreate
from models import (
    create_user, get_all_users, get_user,
    update_user, delete_user, DuplicateEmailError,
)

data = UserCreate(
    first_name="Rahul", last_name="Sharma", email="rahul.sharma@gmail.com",
    phone="9876543210", gender="Male", date_of_birth="2002-05-15",
    department="Engineering", designation="Junior Developer",
).model_dump()

user = create_user(data)
print("CREATED:", user["user_id"], user["email"])

try:
    create_user(data)
except DuplicateEmailError as e:
    print("DUPLICATE CAUGHT:", e)

print("ALL:", len(get_all_users()), "| SEARCH 'sharma':", len(get_all_users("sharma")))
print("ONE:", get_user(user["user_id"])["first_name"])

data["designation"] = "Developer"
print("UPDATED:", update_user(user["user_id"], data)["designation"])
print("UPDATE MISSING USER:", update_user(99999, data))

print("DELETED:", delete_user(user["user_id"]))
print("DELETE AGAIN:", delete_user(user["user_id"]))