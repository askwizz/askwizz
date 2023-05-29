from abc import ABC, abstractmethod
from itertools import starmap
import json
import os
from pathlib import Path
import numpy as np
import pandas as pd


class Database(ABC):
    @abstractmethod
    def insert_references(self, ids: np.ndarray[np.int64], texts: list[str]) -> None:
        """
        Inserts references into the database.
        """

    @abstractmethod
    def find_references(self, ids: list[str]) -> dict[int, str]:
        """
        Finds references in the database by ids.
        """


class InMemoryDatabase(Database):
    def __init__(self) -> None:
        self.references: dict[int, str] = {}
        super().__init__()

    def insert_references(self, ids: np.ndarray[np.int64], texts: list[str]):
        for id_, text in zip(ids, texts):
            self.references[id_] = text

    def find_references(self, ids: list[str]) -> dict[int, str]:
        int_ids = list(map(int, ids))
        return {k: v for k, v in self.references.items() if k in int_ids}


class PandasDatabase(Database):
    def __init__(self, path: Path) -> None:
        if path.suffix != ".csv":
            raise ValueError(
                f"Wrong file type for database, got {path} but expected CSV file"
            )
        self.path = path
        super().__init__()

    def insert_references(self, ids: np.ndarray[np.int64], texts: list[str]):
        dataframe_to_add = pd.DataFrame.from_dict(
            list(starmap(lambda id_, text: {"id": id_, "text": text}, zip(ids, texts)))
        )
        dataframe_to_add.to_csv(
            self.path, mode="a", header=not os.path.exists(self.path), index=False
        )

    def find_references(self, ids: list[str]) -> dict[int, str]:
        pandas_database = pd.read_csv(self.path)
        df_with_indices = json.loads(pandas_database.loc[ids, "text"].to_json())
        return {int(k): v for k, v in df_with_indices.items()}
