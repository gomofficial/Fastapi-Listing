import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
import asyncio

import json

from tests.test_engine import TestingSessionLocal
from tests.user_utils import  user_authentication_headers, get_random_user
from tests.listing_utils import get_random_listing

from main import app
from operations.users import UsersOperation
from operations.listings import ListingOperation

from .test_engine import client


global_user_in = get_random_user()
global_response = client.post(
    f"/listing/",
    content=global_user_in.model_dump_json()
)
global_user_in2 = get_random_user()
global_response2 = client.post(
    f"/listing/",
    content=global_user_in2.model_dump_json()
)
db = TestingSessionLocal()
global_user_db = UsersOperation.get_user_profile(db, username=global_user_in.username)
global_user_db2 = UsersOperation.get_user_profile(db, username=global_user_in2.username)
asyncio.run(db.close())

# headers  = user_authentication_headers(client=client, username=global_user_in.username, password=global_user_in.password)
# headers2 = user_authentication_headers(client=client, username=global_user_in2.username, password=global_user_in2.password)


async def read_listings():
    listing_in = get_random_listing()

    response = client.post(
        "/listings/",
        content=listing_in.model_dump_json(),
        headers= await user_authentication_headers(client=client, username=global_user_in.username, password=global_user_in.password)
    )
    response_get = client.get(
        "/listings/"
    )
    
    post_re_con = json.loads(response.content.decode('utf-8'))
    get_re_con = json.loads(response_get.content.decode('utf-8'))
    
    assert response.status_code == 201
    assert response_get.status_code == 200
    assert post_re_con in get_re_con


async def read_single_listing():
    listing_in = get_random_listing()
    response = client.post(
        "/listings/",
        content=listing_in.model_dump_json(),
        headers=await user_authentication_headers(client=client, username=global_user_in.username, password=global_user_in.password)
    )
    post_re_con = json.loads(response.content.decode('utf-8'))
    response_get = client.get(
        f"/listings/{post_re_con['id']}"
    )
    assert response.status_code == 201
    assert response_get.status_code == 200


async def put_listing():
    listing_in = get_random_listing()
    response = client.post(
        "/listings/",
        content=listing_in.model_dump_json(),
        headers=await user_authentication_headers(client=client, username=global_user_in.username, password=global_user_in.password)
    )
    post_re_con = json.loads(response.content.decode('utf-8'))
    listing_in = get_random_listing()
    response_put = client.put(
        f"/listings/{post_re_con['id']}",
        content=listing_in.model_dump_json(),
        headers=await user_authentication_headers(client=client, username=global_user_in.username, password=global_user_in.password)
    )
    put_re_con = json.loads(response_put.content.decode('utf-8'))

    assert response.status_code == 201
    assert response_put.status_code == 200
    assert post_re_con['address'] != put_re_con['address']


async def delete_listing():
    db = TestingSessionLocal()
    listing_crud = ListingOperation(db)
    listing_in = get_random_listing()
    response = client.post(
        "/listings/",
        content=listing_in.model_dump_json(),
        headers=await user_authentication_headers(client=client, username=global_user_in.username, password=global_user_in.password)
    )
    post_re_con = json.loads(response.content.decode('utf-8'))
    response_delete = client.delete(
        f"/listings/{post_re_con['id']}",
        headers=await user_authentication_headers(client=client, username=global_user_in.username, password=global_user_in.password)
    )
    listing_db = listing_crud.get(db, id=post_re_con['id'])

    db.close()
    assert response.status_code == 201
    assert response_delete.status_code == 200
    assert listing_db is None


async def access_denied_put_listing():
    listing_in = get_random_listing()
    response = client.post(
        "/listings/",
        content=listing_in.model_dump_json(),
        headers=await user_authentication_headers(client=client, username=global_user_in.username, password=global_user_in.password)
    )
    post_re_con = json.loads(response.content.decode('utf-8'))
    listing_in = get_random_listing()
    response_put = client.put(
        f"/listings/{post_re_con['id']}",
        headers=await user_authentication_headers(client=client, username=global_user_in2.username, password=global_user_in2.password),
        content=listing_in.model_dump_json()
    )
    assert response.status_code == 201
    assert response_put.status_code == 403


async def access_denied_delete_listing():
    listing_in = get_random_listing()
    response = client.post(
        "/listings/",
        content=listing_in.model_dump_json(),
        headers=await user_authentication_headers(client=client, username=global_user_in.username, password=global_user_in.password)
    )
    post_re_con = json.loads(response.content.decode('utf-8'))
    response_delete = client.delete(
        f"/listings/{post_re_con['id']}",
        headers=await user_authentication_headers(client=client, username=global_user_in2.username, password=global_user_in2.password)
    )
    assert response.status_code == 201
    assert response_delete.status_code == 403

