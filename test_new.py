from fastapi.testclient import TestClient
from main import app

from tests.user_utils import  user_authentication_headers, get_random_user_update, get_random_user
# from routers.users import UsersOperation

client = TestClient(app)

def test_user_register():
   user_input = get_random_user()
   response = client.post("/account/register", json={"data":user_input.model_dump()})
   print(response.content)
   # assert response.status_code == 201




test_user_register()







# from tests_old.listing import *
# from tests_old.users import *
# from unittest import IsolatedAsyncioTestCase

# class Test(IsolatedAsyncioTestCase):

#    async def test_update_user_information(self):
#       await update_user_information()

#    async def test_read_users_not_authenticated(self):
#       await read_users_not_authenticated()

#    async def test_users_access_denied(self):
#       read_users_access_denied()

#    async def test_read_user(self):
#       await read_user()

#    async def test_no_login(self):
#       await no_login()
        
#    async def test_login(self):
#       await login()

#    async def test_register_existing_username(self):
#       await register_existing_username()

#    async def test_register(self):
#       await register()

#    async def test_read_listings(self):
#       await read_listings()

#    async def test_single_listing(self):
#       await read_single_listing()
        
#    async def test_put_listing(self):
#       await put_listing()

#    async def test_delete_listing(self):
#       await delete_listing()
        
#    async def test_access_denied_put_listing(self):
#       await access_denied_put_listing()

#    async def test_access_denied_delete_listing(self):
#       await access_denied_delete_listing()


