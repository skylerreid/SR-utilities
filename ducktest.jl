using DuckDB, DataFrames, DBInterface

pq_path = "U:\\HTCM\\htcm_scratch\\branch_all.parquet"

con = DBInterface.connect(DuckDB.DB)
DuckDB.query(con, "CREATE VIEW branch_table AS SELECT * FROM read_parquet('$pq_path')")

query1 = """
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

query2 = """
SELECT
    BranchDeviceType,
    COUNT(*) as total_count,
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


@time result_df = DuckDB.query(con, query2) |> DataFrame
if minimum(result_df.min_loading_percent) == 0.0
    select!(result_df, Not(:min_loading_percent))
end

println(result_df)