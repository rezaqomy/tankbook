from pydantic import BaseModel
from pydantic.types import SecretStr
from datetime import datetime

from pydantic.types import conint

# pydantic type that limits the range of primary keys
PrimaryKey = conint(gt=0, lt=2147483647)


class BookTankBase(BaseModel):
    class config:
        orm_mode = True
        from_attributes = True
        validate_assignment = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True

        json_encoders = {
            # custom output conversion for datetime
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if v else None,
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }

