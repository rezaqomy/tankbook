from datetime import datetime

from pydantic import BaseModel
from pydantic.types import SecretStr, conint

from sqlalchemy import Column, DateTime, Integer, event
from src.database.core import Base
# pydantic type that limits the range of primary keys
PrimaryKey = conint(gt=0, lt=2147483647)


#sqlalchemy models ...
class PrimaryKeyMixin(object):
    """Primary key mixin"""

    id = Column(Integer, primary_key=True, autoincrement=True)
    id._creation_order = 9999


class TimeStampMixin(object):
    """Timestamping mixin"""

    created_at = Column(DateTime, default=datetime.utcnow)
    created_at._creation_order = 9998
    updated_at = Column(DateTime, default=datetime.utcnow)
    updated_at._creation_order = 9998

    @staticmethod
    def _updated_at(mapper, connection, target):
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, "before_update", cls._updated_at)

#pydantic models ... 
class BookTankBase(BaseModel):
    class config:
        orm_mode = True
        validate_assignment = True
        arbitrary_types_allowed = True
        anystr_strip_whitespace = True

        json_encoders = {
            # custom output conversion for datetime
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if v else None,
            SecretStr: lambda v: v.get_secret_value() if v else None,
        }



from src.auth.models import *

