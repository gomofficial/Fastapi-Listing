from typing import Dict
from datetime import datetime

from fastapi.testclient import TestClient

from .test_utils import random_email, random_lower_string, random_date
from schema._input import RegisterInput, UpdateUserProfile 
from utils.enums import GenderEnum


def user_authentication_headers(*, client: TestClient, username: str, password: str) -> Dict[str, str]:
    data = {"username": username, "password": password}
    re = client.post("/account/", data=data)
    response = re.json()
    auth_token = responset
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def get_random_user():
    pwd = random_lower_string()+"S"
    return RegisterInput(
        username  =   random_lower_string(),
        full_name =  random_lower_string(),
        email     =      random_email(),
        password  =  pwd,
        gender    =     GenderEnum.MALE,
    )


def get_random_user_update():
    re = UpdateUserProfile(
        username =   random_lower_string(),
        full_name=  random_lower_string(),
        email    =      random_email(),
        gender   =     GenderEnum.MAIL.name,
    )
    del re.password
    return re
    
def get_user_update(**kwargs):
    return UpdateUserProfile(**kwargs)