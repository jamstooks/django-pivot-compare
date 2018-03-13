# Django Pivot Compare

## The Methods

Compares the pivot table methods for:
[Postgres](https://www.postgresql.org/),
[MongoDB](https://www.mongodb.com)
and native [python](https://www.python.org)

### Postgres

Our postgres test will use the
[tablefunc](https://www.postgresql.org/docs/9.2/static/tablefunc.html)
module via the [django-pivot](https://github.com/martsberger/django-pivot)
app.

### MongoDB

Our mongodb test will use
[group aggregation](http://docs.mongodb.org/manual/reference/aggregation/group/)

[ref](https://stackoverflow.com/a/17401008)

### Python

And for our native python test we'll use
[pandas](http://pandas.pydata.org/)

## The Data

This is just a very basic test with the simplest pivot table without summations or aggregations.
All test will start with the exact same data structure (example below) and number of rows (or documents in the case of MongoDB). This test will use **1 Million** rows for input and expect **1000** output rows. Some filtering tests may bring the output list down to 100 or even 10.

### Input (snippet)

Course | Student | Grade
---|---|---
Geography | Ted | 90
Geography | Robin | 95
Geography | Lily | 80
History | Robin | 87
Geography | Marshall | 100
History | Barney | 65
Science | Ted | 73
... | ... | ...

### Expected Output (snippet)

Student | Geography | History | Science
---|---|---|---
Ted | 90 | 89 | 73
Robin | 95 | 87 | 99
Lily | 80 | 95 | 78
... | ... | ...

*Note: the actual data will use the top 1000 names from the US Census and "courses" will be represented by:*

`r'[A-J][001-100]'`
