import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


from main import app
from utils.test_engine import client
from fastapi.testclient import TestClient

from utils.test_engine import TestingSessionLocal
from utils.users import  user_authentication_headers, get_random_user_update, get_random_user
from main import app
from routers import UsersOperation

# from config import settings
# from utils.utils import random_lower_string

client = TestClient(app)


def test_register():
    db = TestingSessionLocal()
    user_crud = UsersOperation(db)
    user_in = get_random_user()
    response = client.post(
        f"/account/register/",
        content=user_in.json()
    )
    user_db = user_crud.get_user(db, username=user_in.username)
    db.close()
    assert response.status_code == 201
    assert user_db.email == user_in.email

def test_register_existing_username():
    user_in = get_random_user()
    response = client.post(
        f"/account/register/",
        content=user_in.json()
    )
    new_user_in = get_random_user()
    new_user_in.username = user_in.username
    response_exising_username = client.post(
        f"/account/register/",
        content=user_in.json()
    )
    assert response.status_code == 201
    assert response_exising_username.status_code == 400

def test_login():
    user_in = get_random_user()
    response = client.post(
        f"/account/register/",
        content=user_in.json()
    )
    login_response = client.post(
        f"/account/token/",
        data={
            'username': user_in.username,
            'password': user_in.password1
        }
    )
    assert response.status_code==201
    assert login_response.status_code==200
    
    tokens = login_response.json()
    assert "access_token" in tokens
    assert tokens["access_token"]
    assert "refresh_token" in tokens
    assert tokens["refresh_token"]


def test_no_login():
    user_in = get_random_user()
    response = client.post(
        f"/account/register/",
        content=user_in.json()
    )
    login_response = client.post(
        f"/account/token/",
        data={
            'username': user_in.username,
            'password': user_in.password1+' fake'
        }
    )
    assert response.status_code==201
    assert login_response.status_code==401


def test_read_user():
    user_in = get_random_user()
    response = client.post(
        f"/account/register/",
        content=user_in.json()
    )
    headers = user_authentication_headers(client=client, username=user_in.username, password=user_in.password1)
    response = client.get(
        f"/account/",
        headers=headers
    )
    assert response.status_code==200


def test_read_users_access_denied():
    user_in1 = get_random_user()
    response = client.post(
        f"/account/register/",
        content=user_in1.json()
    )
    user_in2 = get_random_user()
    response = client.post(
        f"/account/register/",
        content=user_in2.json()
    )
    headers = user_authentication_headers(client=client, username=user_in1.username, password=user_in1.password1)
    response = client.get(
        f"/account/",
        headers=headers
    )
    assert response.status_code==403


def test_read_users_not_authenticated():
    user_in = get_random_user()
    register_response = client.post(
        f"/account/register/",
        content=user_in.json()
    )
    response = client.get(
        f"/account/",
    )
    assert response.status_code==401
    assert register_response.status_code==201


def test_update_user_information():
    db = TestingSessionLocal()
    user_crud = UsersOperation(db)
    
    user_in = get_random_user()
    register_response = client.post(
        f"/account/register/",
        content=user_in.json()
    )

    headers = user_authentication_headers(client=client, username=user_in.username, password=user_in.password1)
    user_in_update = get_random_user_update()
    put_response = client.put(
        f"/account/",
        headers=headers,
        content=user_in_update.json()
    )
    
    db_user_updated = user_crud.get_user(db, username=user_in_update.username)

    db.close()
    
    assert register_response.status_code == 201
    assert put_response.status_code == 200
    assert db_user_updated.full_name == user_in_update.full_name
    assert db_user_updated.username == user_in_update.username
    assert db_user_updated.email == user_in_update.email