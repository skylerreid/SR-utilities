
import duckdb
import pandas as pd
import time

pq_path = "U:\\HTCM\\htcm_scratch\\branch_all.parquet"

con = duckdb.connect()

con.sql(f"CREATE VIEW branch_table AS SELECT * FROM read_parquet('{pq_path}')")

#print headers and first 20 rows of table
# con.sql(f"SELECT * FROM branch_table LIMIT 10").show()

query1 = f"""
SELECT
    BusNum,
    BranchDeviceType,
    BusNomVolt,
    LineLimitPercent,
    (LineLimMVA - LineMVA) AS margin
FROM
    branch_table
WHERE
    LineLimitPercent > 90.0 AND BusNomVolt > 480.0
ORDER BY
    BranchDeviceType, margin
"""

con.sql(query1).show()

query2 = """
SELECT
    BranchDeviceType,
    COUNT(*) as count,
    MAX(LineLimitPercent) as max_loading_percent,
    AVG(LineLimitPercent) as avg_loading_percent,
    MIN(LineLimitPercent) as min_loading_percent
FROM
    branch_table
GROUP BY 
    BranchDeviceType
ORDER BY
    max_loading_percent DESC
"""

#count(*) just gets num rows

query3 = """
SELECT 
    BranchDeviceType,
    COUNT(*) as count,
    COUNT(*) FILTER (WHERE LineLimitPercent > 90) as count_above_90,
    COUNT(*) FILTER (WHERE LineLimitPercent > 75) as count_above_75,
    ROUND(100.0 * COUNT(*) FILTER (WHERE LineLimitPercent > 90) / COUNT(*), 2) as pct_above_90,
    MAX(LineLimitPercent) as max_loading_percent,
    AVG(LineLimitPercent) as avg_loading_percent,
    MIN(LineLimitPercent) as min_loading_percent
FROM 
    branch_table
GROUP BY 
    BranchDeviceType
ORDER BY
    max_loading_percent DESC
"""

start = time.time()
con.sql(query3).show()
print(f"query time: {time.time() - start}")