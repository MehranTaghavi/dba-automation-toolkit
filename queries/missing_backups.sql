SELECT d.name AS DatabaseName
FROM sys.databases AS d
LEFT JOIN msdb.dbo.backupset AS b
    ON d.name = b.database_name AND b.type = 'D'
WHERE d.database_id > 4
GROUP BY d.name
HAVING MAX(b.backup_finish_date) IS NULL
    OR MAX(b.backup_finish_date) < DATEADD(day, -1, GETDATE());
