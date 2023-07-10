import datetime

from pydantic import BaseModel


class SearchHistory(BaseModel):
    id_: str
    user_id: str
    search: str
    created_at: datetime.datetime
