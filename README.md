# pinot-index-benchmarking

### Text Search ([Setup Index](https://docs.pinot.apache.org/basics/indexing/text-search-support#term-query))

#### Queries:
SELECT COUNT(*) 
FROM tpch_lineitem
WHERE TEXT_MATCH(l_comment, "above")

SELECT COUNT(*) 
FROM tpch_lineitem
WHERE l_shipmode = "TRUCK"

SELECT COUNT(*) 
FROM tpch_lineitem
WHERE TEXT_MATCH(l_shipmode,"AIR")

SELECT COUNT(*) 
FROM tpch_lineitem
WHERE TEXT_MATCH(l_shipinstruct,"DELIVER")


# Results
- TPCH lineitem: batch ingestion of 10G with StartreeIndexconfig took 25 minutes
