from pydantic import BaseModel


class SearchHistory(BaseModel):
    id_: str
    user_id: str
    search: str
