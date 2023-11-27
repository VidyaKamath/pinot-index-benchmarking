import time
import requests
from pathlib import Path
from itertools import product
import csv
import statistics

RES_PATH = Path("results.csv")

QUERY_TEMPLATES = {
    "filt_1": """
        SELECT
            SUM(l_extendedprice * l_discount) AS revenue
        FROM
            {table}
        WHERE
            l_discount BETWEEN .06 - 0.01 AND .06 + 0.010001
            AND l_quantity < 24
    """,
    "filt_2": """select count(*) from {table} where l_partkey > 51056""",
    "agg": """SELECT SUM(l_extendedprice), SUM(l_discount) FROM {table}""",
    "filt_3": """SELECT SUM(l_extendedprice) FROM {table} WHERE l_returnflag = 'R'""",
    "filt_4": """SELECT SUM(l_extendedprice) FROM {table} WHERE l_shipdate BETWEEN '1996-12-01' AND '1996-12-31'""",
    "gb_1": """SELECT SUM(l_extendedprice) FROM {table} GROUP BY l_shipdate""",
    "gb_2": """SELECT SUM(l_extendedprice), SUM(l_quantity) FROM {table} GROUP BY l_shipdate""",
    "gb_filt_1": """SELECT SUM(l_extendedprice) FROM {table} WHERE l_shipdate BETWEEN '1995-01-01' AND '1996-12-31' GROUP BY l_shipdate""",
    "gb_filt_2": """SELECT SUM(l_extendedprice) FROM {table} WHERE l_shipmode in ('RAIL', 'FOB') AND l_receiptdate BETWEEN '1997-01-01' AND '1997-12-31' GROUP BY l_shipmode""",
    "distinct": """SELECT DISTINCT l_shipmode FROM {table}""",
}


# used duckdb on the raw tbl to get the percentiles. (pinot doesn't allow quantile_disc on date columns)
# select quantile_disc(L_SHIPDATE, [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]) from lineitem;
SELECTIVITY_QUERIES = {
    f"gb_filt_sel_{percent}": f"""SELECT SUM(l_extendedprice) FROM {{table}} WHERE l_receiptdate < {lim}"""
    for percent, lim in zip(
        [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        ["1992-01-02", "1992-10-28", "1993-06-26", "1994-02-21", "1994-10-20", "1995-06-17", "1996-02-13", "1996-10-11", "1997-06-08", "1998-02-04", "1998-12-01"],
    )
}


def make_query(template, table):
    return template.format(table=table)


def run_query(query, name="query"):
    URI = "http://fa23-cs511-011.cs.illinois.edu:9000"
    resp = requests.post(URI + "/sql", json={"sql": query}, params={"name": name})
    assert resp, f"Query {query} failed, {resp}"
    exc = resp.json()["exceptions"]
    assert not exc, "Got exceptions: " + str(exc)


def run_benchmark(query, name="query", n=10):
    # Run the query 10 times and measure execution time
    times = []
    for i in range(n):
        start_time = time.time()
        run_query(query, name=f"{name}_{i}")
        end_time = time.time()

        execution_time = end_time - start_time
        times.append(execution_time)
        print(f"Execution time: {execution_time} seconds")
    return times


def write_results(name, table, times):
    # append the execution times as a csv row
    if not RES_PATH.exists() or RES_PATH.stat().st_size == 0:
        # write header
        with RES_PATH.open("w") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "table", "run_name", "time"])

    with RES_PATH.open("a") as f:
        writer = csv.writer(f)
        for i, time in enumerate(times):
            writer.writerow([name, table, f"run_{i}", time])


def main():
    TABLES = list(f"tpch_lineitem_{size}{('_' * bool(idx)) + idx}" for size, idx in product(("1g", "10g"), ("no_idx", "bitmap_idx", ""),))
    # Run the queries
    RES_PATH.unlink(missing_ok=True)
    for table, (name, query) in product(
        TABLES,
        # QUERY_TEMPLATES.items(),
        SELECTIVITY_QUERIES.items(),
    ):
        print(f"Running {name} on {table}")
        query = make_query(query, table)
        times = run_benchmark(query, name)
        # print(query)
        write_results(name, table, times)


if __name__ == "__main__":
    main()
