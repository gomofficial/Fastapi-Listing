from tests.listing import *
from tests.users import *
from unittest import IsolatedAsyncioTestCase

class Test(IsolatedAsyncioTestCase):

    async def test_update_user_information(self):
       await update_user_information()

    async def test_read_users_not_authenticated(self):
        await read_users_not_authenticated()

    async def test_users_access_denied(self):
        await read_users_access_denied()

    async def test_read_user(self):
        await read_user()

    async def test_no_login(self):
        await no_login()
        
    async def test_login(self):
        await login()

    async def test_register_existing_username(self):
        await register_existing_username()

    async def test_register(self):
        await register()

    async def test_read_listings(self):
        await read_listings()

    async def test_single_listing(self):
        await read_single_listing()
        
    async def test_put_listing(self):
        await put_listing()

    async def test_delete_listing(self):
        await delete_listing()
        
    async def test_access_denied_put_listing(self):
        await access_denied_put_listing()

    async def test_access_denied_delete_listing(self):
        await access_denied_delete_listing()


