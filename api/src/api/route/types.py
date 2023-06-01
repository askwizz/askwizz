from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    confluence_space_key: str
