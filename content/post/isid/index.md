---
title: Testing primary keys in Impala/Hive
subtitle: Unlike standard SQL databases, Hadoop based Imapla and Hive do not enforce primary keys. This function helps to test for them regardless.


# Summary for listings and search engines
summary: In this post I show how you can test whether a combination of columns forms a primary key using Impala or Hive

# Link this post with a project
projects: []

# Date published
date: "2022-02-01T00:00:00Z"

# Date updated
lastmod: "2022-02-01T00:00:00Z"

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
- Academic

#categories:
#- Demo
#- 教程
---

Primary keys are perhaps the most basic building block of relational data modelling. If you have a table containing data, (one of) the first question(s) you 
should argueably ask is "what are the dimensions of the data?". In Economics this is sometimes referred to as the "level of observation". 
More formally it is a set of keys ("columns") that uniquely identify a row in the table. In classical database archtictures such as OracleSQL you need to delare
the primary keys of a table upon creating the table. In distributed systems such as Hadoop and its SQL engine and table metastore Hive however, primary keys are not
declared explicitely. If they are not documented anywhere this can lead to confusion. In any case, it is useful to know how to test whether certain keys do constitute
a set of primary keys. The following code helps you achieve this:
```sql
SELECT CASE WHEN MAX(tab.rows_count_each) > 1
            THEN CAST(0 AS BOOLEAN)
            ELSE CAST(1 AS BOOLEAN)
       END AS 'Primary_Keys'
FROM (SELECT COUNT(*) AS rows_count_each
      FROM database.table_name
      GROUP BY var1, var2) tab
```

For those of you with less of a background in SQL, the above is equivalent to `python`:

```python
df.set_index(['var1','var2']).index.is_unique
```

or `Stata`'s:
```
isid var1 var2
```
	