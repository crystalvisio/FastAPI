import pytest
from jose import jwt
from app import schemas, config

# Testing Route for Root
def test_root(client):
    res = client.get("/")

    print(res.json())

    assert res.json().get("message") == "Welcome to FastAPI.com"
    assert res.status_code == 200

# Testing Route for Creating New User
def test_createUser(client):
    res = client.post("/user", json={"name": "TestUser", "email": "testuser@user.com", "password": "12345"})

    print(res.json())

    new_user = schemas.UserBase(**res.json())
    
    assert new_user.email == "testuser@user.com"
    assert res.status_code == 201

# Testing Route for Logging Users
def test_login(client, test_user):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})

    print(res.json())

    _tokenData = schemas.Token(**res.json())
    _token = _tokenData.access_token

    # Decode the token and validate payload
    payload = jwt.decode(_token, config.settings.secret_key, algorithms=[config.settings.algorithm])
    _id = payload.get("user_id")

    assert _id == test_user["id"]
    assert _tokenData.token_type == "bearer"
    assert res.status_code == 200

# Testing Route for Invalid Credentials
@pytest.mark.parametrize("email, password, statusCode", [
    ("wrongemail@gmail.com", "johndoe", 403),
    ("johndoe@email.com", "wrongpassword", 403),
    ("wrongemail@email.com", "wrongpassword", 403),
    (None, "johndoe", 422),
    ("johndoe@email.com", None, 422)
])
def test_invalidCredentials(client, email, password, statusCode):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == statusCode
