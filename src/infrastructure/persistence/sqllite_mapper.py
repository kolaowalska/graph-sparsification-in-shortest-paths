class SQLiteMapper:
    """
    stub for a future [DATA MAPPER] that handles mapping between Domain Entities and database rows
    """
    def __init__(self, connection_string: str):
        self._connection_string = connection_string
        print(f"[stub] initialized SQLiteDataMapper connecting to {connection_string}")

    def to_domain(self, row: dict) -> object:
        # TODO: implement mapping logic
        pass

    def to_row(self, entity: object) -> dict:
        # TODO: implement mapping logic
        pass
