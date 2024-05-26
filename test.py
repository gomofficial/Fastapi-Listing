from tests.listing import *
from tests.users import *

from unittest import IsolatedAsyncioTestCase

class Test(IsolatedAsyncioTestCase):

    async def test_functionality(self):
       await test_update_user_information()


# test_read_users_not_authenticated()
# test_read_users_access_denied()
# test_read_user()
# test_no_login()
# test_login()
# test_register_existing_username()
# test_register()

# test_read_listings()
# test_read_single_listing()
# test_put_listing()
# test_delete_listing()
# test_access_denied_put_listing()
# test_access_denied_delete_listing()


