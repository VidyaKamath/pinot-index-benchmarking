from locust import FastHttpUser, task, HttpUser

import requests
import random


# range index queries

query0 = """
SELECT
     SUM(l_extendedprice * l_discount) AS revenue
FROM
     tpch_lineitem
WHERE
     l_discount BETWEEN .06 - 0.01 AND .06 + 0.010001
     AND l_quantity < 24
"""

query1 = """
select count(*) from tpch_lineitem where l_partkey > 51056
"""


# star tree queries
query0 = """
SELECT SUM(l_extendedprice), SUM(l_discount) FROM tpch_lineitem
"""

query1 = """
SELECT SUM(l_extendedprice) FROM tpch_lineitem WHERE l_returnflag = 'R'
"""

query2 = """
SELECT SUM(l_extendedprice) FROM tpch_lineitem WHERE l_shipdate BETWEEN '1996-12-01' AND '1996-12-31'
"""

query3 = """
SELECT SUM(l_extendedprice) FROM tpch_lineitem GROUP BY l_shipdate
"""

query4 = """
SELECT SUM(l_extendedprice), SUM(l_quantity) FROM tpch_lineitem GROUP BY l_shipdate
"""
query5 = """
SELECT SUM(l_extendedprice) FROM tpch_lineitem WHERE l_shipdate BETWEEN '1995-01-01' AND '1996-12-31' GROUP BY l_shipdate
"""

query6 = """
SELECT SUM(l_extendedprice) FROM tpch_lineitem WHERE l_shipmode in ('RAIL', 'FOB') AND l_receiptdate BETWEEN '1997-01-01' AND '1997-12-31' GROUP BY l_shipmode
"""

class PinotUser(FastHttpUser):
    @task
    def run_q0(self):
        
        with super().rest("POST", "/query/sql", json={"sql": query0}, name="q0") as r:
            if r.status_code == requests.codes.ok:
                # print("/query/sql   - q1" + ': success (200)')
                pass
            elif r.status_code == 0:
                print("/query/sql - q0" + ': success (0)')
                r.success()
            else:
                print("/query/sql - qO" + ': failure (' + str(r.status_code) + ')')
                r.failure(r.status_code)
                
    @task
    def run_q1(self):
        
        with super().rest("POST", "/query/sql", json={"sql": query1}, name="q1") as r:
            if r.status_code == requests.codes.ok:
                # print("/query/sql   - q1" + ': success (200)')
                pass
            elif r.status_code == 0:
                print("/query/sql - q1" + ': success (0)')
                r.success()
            else:
                print("/query/sql - q1" + ': failure (' + str(r.status_code) + ')')
                r.failure(r.status_code)
    @task
    def run_q2(self):
        
        with super().rest("POST", "/query/sql", json={"sql": query2}, name="q2") as r:
            if r.status_code == requests.codes.ok:
                # print("/query/sql   - q1" + ': success (200)')
                pass
            elif r.status_code == 0:
                print("/query/sql - q2" + ': success (0)')
                r.success()
            else:
                print("/query/sql - q2" + ': failure (' + str(r.status_code) + ')')
                r.failure(r.status_code)
    
    @task
    def run_q3(self):
        
        with super().rest("POST", "/query/sql", json={"sql": query3}, name="q3") as r:
            if r.status_code == requests.codes.ok:
                # print("/query/sql   - q1" + ': success (200)')
                pass
            elif r.status_code == 0:
                print("/query/sql - q3" + ': success (0)')
                r.success()
            else:
                print("/query/sql - q3" + ': failure (' + str(r.status_code) + ')')
                r.failure(r.status_code)
    @task
    def run_q4(self):
        
        with super().rest("POST", "/query/sql", json={"sql": query4}, name="q4") as r:
            if r.status_code == requests.codes.ok:
                # print("/query/sql   - q1" + ': success (200)')
                pass
            elif r.status_code == 0:
                print("/query/sql - q4" + ': success (0)')
                r.success()
            else:
                print("/query/sql - q4" + ': failure (' + str(r.status_code) + ')')
                r.failure(r.status_code)

    @task
    def run_q5(self):
        
        with super().rest("POST", "/query/sql", json={"sql": query5}, name="q5") as r:
            if r.status_code == requests.codes.ok:
                # print("/query/sql   - q1" + ': success (200)')
                pass
            elif r.status_code == 0:
                print("/query/sql - q5" + ': success (0)')
                r.success()
            else:
                print("/query/sql - q5" + ': failure (' + str(r.status_code) + ')')
                r.failure(r.status_code)
    
    @task
    def run_q6(self):
        
        with super().rest("POST", "/query/sql", json={"sql": query6}, name="q6") as r:
            if r.status_code == requests.codes.ok:
                # print("/query/sql   - q1" + ': success (200)')
                pass
            elif r.status_code == 0:
                print("/query/sql - q6" + ': success (0)')
                r.success()
            else:
                print("/query/sql - q6" + ': failure (' + str(r.status_code) + ')')
                r.failure(r.status_code)
