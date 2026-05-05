"""Transaction Class."""

class Transaction:
    """Represents a MyEdenred account transaction."""

    def __init__(self, transaction):
        self._data = transaction
        
    @property
    def date(self):
        return self._data["transactionDate"]

    @property
    def name(self):
        return self._data["transactionName"]

    @property
    def amount(self) -> str:
        """Return raw amount as provided by the upstream parser."""
        return str(self._data["amount"])
