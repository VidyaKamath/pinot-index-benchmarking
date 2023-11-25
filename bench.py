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
    "filt_4":    """SELECT SUM(l_extendedprice) FROM {table} WHERE l_shipdate BETWEEN '1996-12-01' AND '1996-12-31'""",
    "gb_1":    """SELECT SUM(l_extendedprice) FROM {table} GROUP BY l_shipdate""",
    "gb_2": """SELECT SUM(l_extendedprice), SUM(l_quantity) FROM {table} GROUP BY l_shipdate""",
    "gb_filt_1": """SELECT SUM(l_extendedprice) FROM {table} WHERE l_shipdate BETWEEN '1995-01-01' AND '1996-12-31' GROUP BY l_shipdate""",
    "gb_filt_2":  """SELECT SUM(l_extendedprice) FROM {table} WHERE l_shipmode in ('RAIL', 'FOB') AND l_receiptdate BETWEEN '1997-01-01' AND '1997-12-31' GROUP BY l_shipmode""",
    "distinct": """SELECT DISTINCT l_shipmode FROM {table}""",
}


# SELECTIVITY_QUERIES = {
#     "gb_filt_0": """""",
#     "gb_filt_10": """""",
#     "gb_filt_20": """""",
#     "gb_filt_30": """""",
#     "gb_filt_40": """""",
#     "gb_filt_50": """""",
#     "gb_filt_60": """""",
#     "gb_filt_70": """""",
#     "gb_filt_80": """""",
#     "gb_filt_90": """""",
#     "gb_filt_100": """""",
# }

def make_query(template, table):
    return template.format(table=table)


def run_query(query, name="query"):
    URI = "http://fa23-cs511-011.cs.illinois.edu:9000"
    resp = requests.post(URI + "/sql", json={"sql": query}, params={"name": name})
    assert resp, f"Query {query} failed, {resp}"
    exc = resp.json()['exceptions']
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
            writer.writerow(["name", "table", *[f"run_{i}" for i in range(10)], "avg", "std"])

    with RES_PATH.open("a") as f:
        writer = csv.writer(f)
        writer.writerow([name, table, *times, statistics.mean(times), statistics.stdev(times)])


def main():
    # Run the queries
    for table, (name, query) in product(["tpch_lineitem_1g_no_idx", "tpch_lineitem_10g", "tpch_lineitem_10g_no_idx"], QUERY_TEMPLATES.items()):
        query = make_query(query, table)
        times = run_benchmark(query, name)
        write_results(name, table, times)
        # break


if __name__ == "__main__":
    main()
