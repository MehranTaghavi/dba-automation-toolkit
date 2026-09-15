SELECT
    r.session_id AS SessionId,
    r.status AS Status,
    r.total_elapsed_time / 1000 AS ElapsedTimeSeconds,
    t.text AS QueryText
FROM sys.dm_exec_requests AS r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) AS t
WHERE r.total_elapsed_time > 60000
    AND r.session_id <> @@SPID;
