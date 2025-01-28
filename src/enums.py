from enum import StrEnum


class BaseEnum(StrEnum):

    pass

class UserRoles(BaseEnum):
    CUSTOMER = 'customer'
    ADMIN = 'admin'
    AUTHOR = 'author'
