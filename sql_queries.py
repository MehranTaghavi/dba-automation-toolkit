"""Load SQL Server health checks and provide sample results."""

from pathlib import Path


def load_query(filename: str) -> str:
    """Read a query from the project's SQL query directory."""
    query_path = Path(__file__).parent / "queries" / filename
    return query_path.read_text(encoding="utf-8")

QUERIES = {
    "missing_backups": load_query("missing_backups.sql"),
    "high_index_fragmentation": load_query("high_index_fragmentation.sql"),
    "long_running_queries": load_query("long_running_queries.sql"),
}

SAMPLE_RESULTS = {
    "missing_backups": [
        {"DatabaseName": "SalesDb"},
        {"DatabaseName": "ReportingDb"},
    ],
    "high_index_fragmentation": [
        {
            "SchemaName": "dbo",
            "TableName": "Orders",
            "IndexName": "IX_Orders_CreatedAt",
            "FragmentationPercent": 42.75,
        },
    ],
    "long_running_queries": [
        {
            "SessionId": 57,
            "Status": "running",
            "ElapsedTimeSeconds": 128,
            "QueryText": "SELECT * FROM dbo.Orders",
        },
    ],
}
