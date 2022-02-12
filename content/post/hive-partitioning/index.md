---
title: How to fix Hive table partioning
subtitle: 


# Summary for listings and search engines
summary: In this post I show how you can fix a hive table, where partitioned data is not picked up correctly. 

# Link this post with a project
projects: []

# Date published
date: "2022-02-15T00:00:00Z"

# Date updated
lastmod: "2020-02-15T00:00:00Z"

# Is this an unpublished draft?
draft: false

# Show this page in the Featured widget?
featured: false

# Featured image
# Place an image named `featured.jpg/png` in this page's folder and customize its options here.
image:
  caption: 'Image credit: [**Image credits**](https://pixabay.com/de/photos/honigbienen-insekten-bienenstock-337695/)'
  focal_point: ""
  placement: 2
  preview_only: false

authors:
- admin


tags:
- Data Engineering

#categories:
#- Demo
#- 教程
---




In this article I show how you can fix partition tables in hive.
Partitioning tables is the best practice on distributed systems, in particular for large datasets.
On HDFS For example, a 1280MB large data set is automatically split in ten files of 128MB, in order to ease the process of parallelization.
If you expose such a data set as a table on Hive, in order to be able to query it, the underlying algorithm
will have to read in all ten files to do the computation you asked for. Consider the following query: 

    SELECT avg(GDP)
	FROM mydb.country_table
	WHERE region='ASIA'
	
In such a query, all files will first be scanned and filtered for `continent='ASIA'`. It would be much more efficient
if we knew in advance whether any given file contains any such records. Table partioning achieves exactly that. You can use Hive to directly create a partitioned table from another existing table for example. 

However, sometimes the underlying data might not be available as a table, but is simply written to HDFS from an external source. Consider the following minimal example:
		
	country_table
	├── continent='ASIA'
	│   ├── 0bac803e32dc42ae83fddfd029cbdebc.parquet
	│   └── ...
	├── continent='EUROPE'
	│   ├── e6ab24a4f45147b49b54a662f0c412a3.parquet
	│   └── ...
	└── ...

The data is stored in 'subfolders' that will allow Hive to understand these as partitions (e.g. from python pandas you could create such a structure using `df.to_parquet(path='...\country_table', partition_cols=['continent']`).
```sql
CREATE EXTERNAL TABLE mydb.country_table
-- below specify the HDFS path to any file to infer the schema
LIKE PARQUET '/.../.../country_table/continent=ASIA/0bac803e32dc42ae83fddfd029cbdebc.parquet'
-- this is where the magic happens: We partition the table!
PARTITIONED BY (continent STRING)
STORED AS PARQUET
LOCATION '/.../.../country_table'
```	
If you are on this page you likely have experienced yourself that this does not work. While the table meta data is available for some reason it does not return any data when queried:







This is because Hive needs to update its metadata (good read for the details [here](https://analyticshut.com/msck-repair-fixing-partitions-in-hive-table/)). 	
Luckily there is a simple fix: 

```sql
MSCK REPAIR TABLE mydb.country_table
```
After which you should update the table meta data:

    INVALIDATE METADATA mydb.country_table
	
	
	
