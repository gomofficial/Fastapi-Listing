from .user_utils import  user_authentication_headers, get_random_user_update, get_random_user
from .test_engine import client

def test_user_register():
   # user_input = get_random_user()
   response = client.get("/listing/all")
   assert response.status_code == 200

def test_user_register():
   user_input = get_random_user()
   response = client.post("/account/register", content={"data":user_input.model_dump()})
   # assert response.status_code == 200
   print(response.content)