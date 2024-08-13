import pytest
from fastapi.testclient import TestClient
from tests import db_test
from app import database, main, oauth2, models


# Fixture to create a test user
@pytest.fixture
def test_user(client):
    user_data = {
        "name": "John Doe",
        "email": "johndoe@email.com",
        "password": "johndoe"
    }
    res = client.post("/user", json=user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


# Fixture to create a second test user
@pytest.fixture
def demo_user(client):
    user_data = {
        "name": "DemoUser",
        "email": "demouser@email.com",
        "password": "demouser"
    }
    res = client.post("/user", json=user_data)
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


# Fixture to reset the database before each test
@pytest.fixture(scope='function')
def session():
    database.Base.metadata.drop_all(bind=db_test.engine)
    database.Base.metadata.create_all(bind=db_test.engine)
    yield next(db_test.get_test_db_session())
    db_test.get_test_db_session().close()


# Initialize the TestClient with overridden dependency
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    main.app.dependency_overrides[database.get_db] = override_get_db
    yield TestClient(main.app)


# Access_Token fixture
@pytest.fixture
def demo_token(test_user):
    return oauth2.create_access_token({"user_id": test_user["id"]})


# Authorize Client Fixture
@pytest.fixture()
def authorize_client(client, demo_token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {demo_token}"
    }
    yield client


# Create Demo Post Fixture
@pytest.fixture
def test_create_posts(session, test_user, demo_user):
    demo_posts = [
        models.Post(title="first_title", content="first_content", user_id=test_user["id"]),
        models.Post(title="2nd_title", content="2nd_content", user_id=test_user["id"]),
        models.Post(title="3rd_title", content="3rd_content", user_id=test_user["id"]),
        models.Post(title="4th_title", content="4th_content", user_id=demo_user["id"])
    ]
    
    session.add_all(demo_posts)
    session.commit()

    return session.query(models.Post).all()
