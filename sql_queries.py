"""T-SQL health checks used by the automation tool."""

QUERIES = {
    "missing_backups": """
        SELECT d.name AS DatabaseName
        FROM sys.databases AS d
        LEFT JOIN msdb.dbo.backupset AS b
            ON d.name = b.database_name AND b.type = 'D'
        WHERE d.database_id > 4
        GROUP BY d.name
        HAVING MAX(b.backup_finish_date) IS NULL
            OR MAX(b.backup_finish_date) < DATEADD(day, -1, GETDATE());
    """,
    "high_index_fragmentation": """
        SELECT
            OBJECT_SCHEMA_NAME(ips.object_id) AS SchemaName,
            OBJECT_NAME(ips.object_id) AS TableName,
            i.name AS IndexName,
            CAST(ips.avg_fragmentation_in_percent AS DECIMAL(6, 2))
                AS FragmentationPercent
        FROM sys.dm_db_index_physical_stats(
            DB_ID(), NULL, NULL, NULL, 'LIMITED'
        ) AS ips
        JOIN sys.indexes AS i
            ON ips.object_id = i.object_id AND ips.index_id = i.index_id
        WHERE ips.avg_fragmentation_in_percent > 30.0
            AND i.name IS NOT NULL;
    """,
    "long_running_queries": """
        SELECT
            r.session_id AS SessionId,
            r.status AS Status,
            r.total_elapsed_time / 1000 AS ElapsedTimeSeconds,
            t.text AS QueryText
        FROM sys.dm_exec_requests AS r
        CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) AS t
        WHERE r.total_elapsed_time > 60000
            AND r.session_id <> @@SPID;
    """,
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
