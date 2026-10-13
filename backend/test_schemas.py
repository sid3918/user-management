from pydantic import ValidationError
from schemas import UserCreate

good = UserCreate(
    first_name="  Rahul ",
    last_name="Sharma",
    email="rahul.sharma@example.com",
    phone="9876543210",
    gender="Male",
    date_of_birth="2002-05-15",
    department="Engineering",
    designation="Junior Developer",
)
print("VALID:", good)

try:
    UserCreate(
        first_name="",
        last_name="Sharma",
        email="not-an-email",
        phone="123",
        gender="Unknown",
        date_of_birth="2999-01-01",
    )
except ValidationError as e:
    print("\nINVALID, errors found:")
    for err in e.errors():
        print(" -", err["loc"][0], "->", err["msg"])