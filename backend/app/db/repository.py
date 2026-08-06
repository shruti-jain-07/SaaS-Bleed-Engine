from typing import Any, List
from sqlalchemy.orm import Session


class TransactionRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all_transactions(self) -> List[Any]:
        """Fetch all transactions from the database (stub for analytics service)."""
        return []