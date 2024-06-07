from .user_utils import  user_authentication_headers, get_random_user_update, get_random_user
from .test_engine import client




def test_get_all_listings():
   # user_input = get_random_user()
   response = client.get("/listing/all")
   assert response.status_code == 200

def test_post_listings():
   # user_input = get_random_user()
   response = client.get("/listing/all")
   assert response.status_code == 200
