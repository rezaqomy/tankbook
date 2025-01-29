
from datetime import datetime


from sqlalchemy import Column, DateTime, Integer, event


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

