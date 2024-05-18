from enum import Enum


class GenderEnum(str,Enum):
    FEMALE = "FEMALE"
    MALE = "MALE"
    NOT_SPECIFIED = "NOT_SPECIFIED"

class TypeEnum(str,Enum):
    APARTMENT = "APARTMENT"
    HOUSE = "HOUSE"
