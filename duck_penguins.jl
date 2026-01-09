using DuckDB, DataFrames, DBInterface

con = DBInterface.connect(DuckDB.DB)

DuckDB.query(con, "CREATE VIEW penguins AS SELECT * FROM read_csv('U:\\NAERM\\naerm_scratch\\penguins.csv')")

query1 = """
SELECT
    species,
    MAX(TRY_CAST(flipper_length_mm AS INTEGER)) as max_flipper_length,
    MIN(TRY_CAST(flipper_length_mm AS INTEGER)) as min_flipper_length,
    AVG(TRY_CAST(flipper_length_mm AS DOUBLE)) as avg_flipper_length
FROM
    penguins
WHERE
    flipper_length_mm IS NOT NULL 
    AND flipper_length_mm != ''
    AND TRY_CAST(flipper_length_mm AS INTEGER) IS NOT NULL
GROUP BY   
    species
ORDER BY
    avg_flipper_length DESC
"""

@time result_df = DuckDB.query(con, query1) |> DataFrame