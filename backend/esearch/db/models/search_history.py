from sqlalchemy import Column, String
from sqlalchemy.orm import Session

from esearch.core.search_history.definition import SearchHistory
from esearch.db.engine import Base


class SearchHistoryRow(Base):
    __tablename__ = "search_history"

    id = Column(String(20), primary_key=True)  # noqa: A003
    user_id = Column(String(200), nullable=False)
    search = Column(String(1024), nullable=False)


def convert_from_db_to_entity(search: SearchHistoryRow) -> SearchHistory:
    return SearchHistory(
        id_=search.id,  # type: ignore
        user_id=search.user_id,  # type: ignore
        search=search.search,  # type: ignore
    )


def convert_from_entity_to_db(search: SearchHistory) -> SearchHistoryRow:
    return SearchHistoryRow(
        id=search.id_,
        user_id=search.user_id,
        search=search.search,
    )


def save_search_into_db(db: Session, search: SearchHistory) -> None:
    db.add(convert_from_entity_to_db(search))
    db.commit()
