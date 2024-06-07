from .user_utils import  user_authentication_headers, get_random_user_update, get_random_user
from .test_engine import client
from .test_engine import TestingSessionLocal
from .user_utils import  user_authentication_headers, get_random_user
from .listing_utils import get_random_listing
import json


global_user_in = get_random_user()
global_response = client.post(
    f"/account/register",
    json=global_user_in.model_dump_json()
)
global_user_in2 = get_random_user()
global_response2 = client.post(
    f"/account/register",
    json=global_user_in2.model_dump_json()
)

def get_all_listings():
   # user_input = get_random_user()
   response = client.get("/listing/all")
   assert response.status_code == 200

def read_listings():
    listing_in = get_random_listing()

    response = client.post(
        "/listing",
        json=listing_in.model_dump_json(),
        headers= user_authentication_headers(client=client, username=global_user_in.username, password=global_user_in.password)
    )
    response_get = client.get(
        "/listing/all"
    )
    
    post_re_con = json.loads(response.content.decode('utf-8'))
    get_re_con = json.loads(response_get.content.decode('utf-8'))
    
    assert response.status_code == 201
    assert response_get.status_code == 200
    assert post_re_con in get_re_con
   
def read_single_listing():
   listing_in = get_random_listing()
   response = client.post(
      "/listing",
      json=listing_in.model_dump_json(),
      headers=user_authentication_headers(client=client, username=global_user_in.username, password=global_user_in.password)
   )
   post_re_con = json.loads(response.content.decode('utf-8'))
   response_get = client.get(
      f"/listing/?id={post_re_con["id"]}"
   )
   assert response.status_code == 200
   assert response_get.status_code == 200


def put_listing():
    listing_in = get_random_listing()
    response = client.post(
        "/listing",
        json=listing_in.model_dump_json(),
        headers=user_authentication_headers(client=client, username=global_user_in.username, password=global_user_in.password)
    )
    post_re_con = json.loads(response.content.decode('utf-8'))
    listing_in = get_random_listing()
    response_put = client.put(
        f"/listing/?id={post_re_con['id']}",
        json=listing_in.model_dump_json(),
        headers=user_authentication_headers(client=client, username=global_user_in.username, password=global_user_in.password)
    )
    put_re_con = json.loads(response_put.content.decode('utf-8'))

    assert response.status_code == 200
    assert response_put.status_code == 200
    assert post_re_con['address'] != put_re_con['address']

def delete_listing():
    listing_in = get_random_listing()
    response = client.post(
        "/listings",
        json=listing_in.model_dump_json(),
        headers=user_authentication_headers(client=client, username=global_user_in.username, password=global_user_in.password)
    )
    post_re_con = json.loads(response.content.decode('utf-8'))
    response_delete = client.delete(
        f"/listing/?id={post_re_con['id']}",
        headers=user_authentication_headers(client=client, username=global_user_in.username, password=global_user_in.password)
    )
    assert response.status_code == 200
    assert response_delete.status_code == 200

    