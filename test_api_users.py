from tests.user_utils import  user_authentication_headers, get_random_user_update, get_random_user
from tests.test_engine import client


def test_register():
   user_input = get_random_user()
   response = client.post("/account/register", json={"data":user_input.model_dump_json()})
   assert response.status_code == 200


def test_register_existing_username():
    user_in = get_random_user()
    response = client.post(f"/account/register",json={"data":user_in.model_dump_json()})
    new_user_in = get_random_user()
    new_user_in.username = user_in.username
    response_exising_username = client.post(f"/account/register",json={"data":new_user_in.model_dump_json()})
    assert response.status_code == 200
    assert response_exising_username.status_code == 400

def test_login():
    user_in = get_random_user()
    response = client.post(f"/account/register",json={"data":user_in.model_dump_json()})
    login_response = client.post(
        f"/account/token",
        data={
            'username': user_in.username,
            'password': user_in.password
        })
    assert response.status_code==200
    assert login_response.status_code==200


def test_no_login():
    user_in = get_random_user()
    response = client.post(f"/account/register",json={"data":user_in.model_dump_json()})
    login_response = client.post(
        f"/account/token",
        data={
            'username': user_in.username,
            'password': user_in.password+' fake'
        })
    assert response.status_code==200
    assert login_response.status_code==401


def test_read_user():
    user_in = get_random_user()
    response = client.post(
        f"/account/register",
        json={"data":user_in.model_dump_json()})
    headers = user_authentication_headers(client=client, username=user_in.username, password=user_in.password)
    response = client.get(f"/account/profile",headers=headers)
    assert response.status_code==200


def test_read_users_not_authenticated():
    user_in = get_random_user()
    register_response = client.post(
        f"/account/register",
        json={"data":user_in.model_dump_json()}
    )
    response = client.get(
        f"/account/profile",
    )
    assert response.status_code==401
    assert register_response.status_code==200


def test_update_user_information():
   user_in = get_random_user()
   register_response = client.post(
      f"/account/register",
      json={"data":user_in.model_dump_json()}
   )

   headers = user_authentication_headers(client=client, username=user_in.username, password=user_in.password)
   user_in_update = get_random_user_update()
   put_response = client.put(
      f"/account/update",
      headers=headers,
      json={"data":user_in_update.model_dump_json()}
   )
    
   assert register_response.status_code == 200
   assert put_response.status_code == 200

def test_delete_user_information():
   user_in = get_random_user()
   register_response = client.post(
      f"/account/register",
      json={"data":user_in.model_dump_json()}
   )
   headers = user_authentication_headers(client=client, username=user_in.username, password=user_in.password)
   put_response = client.delete(f"/account/update",headers=headers)

   assert register_response.status_code == 200
   assert put_response.status_code == 200

   