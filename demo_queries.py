# No idx table
SELECT SUM(l_extendedprice), SUM(l_discount) FROM tpch_lineitem_10g_no_idx
SELECT SUM(l_extendedprice) FROM tpch_lineitem_10g_no_idx GROUP BY l_shipdate

# Star tree idx table T=1000
SELECT SUM(l_extendedprice), SUM(l_discount) FROM tpch_lineitem_10g_star_idx_1000
SELECT SUM(l_extendedprice) FROM tpch_lineitem_10g_star_idx_1000 GROUP BY l_shipdate


# No impact queries
# no idx
SELECT DISTINCT l_shipmode FROM tpch_lineitem_10g_no_idx

# star idx
SELECT DISTINCT l_shipmode FROM tpch_lineitem_10g_star_idx_1000


