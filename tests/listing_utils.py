from .user_utils import random_email, random_lower_string, random_date
from schema._input import ListingInput
from utils.enums import TypeEnum

def get_random_listing():
    return ListingInput(
        address=random_lower_string(),
        available_now=True,
        type=TypeEnum.APARTMENT
    )

