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

### Native Text Index ([Setup Index](https://docs.pinot.apache.org/basics/indexing/native-text-index))

#### Queries:
SELECT COUNT(*) 
FROM tpch_lineitem
WHERE TEXT_CONTAINS(l_comment, "above")

SELECT COUNT(*) 
FROM tpch_lineitem
WHERE l_shipmode = "TRUCK"

SELECT COUNT(*) 
FROM tpch_lineitem
WHERE TEXT_CONTAINS(l_shipmode,"AIR")

SELECT COUNT(*) 
FROM tpch_lineitem
WHERE TEXT_CONTAINS(l_shipinstruct,"DELIVER")

# Results
- TPCH lineitem: batch ingestion of 1G without any index took 00:02:48
- TPCH lineitem: batch ingestion of 10G without any index took 00:24:00
- TPCH lineitem: batch ingestion of 10G with StartreeIndexconfig took 00:25:00
