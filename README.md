# Django Pivot Compare

Compares the pivot table methods for:
[Postgres](https://www.postgresql.org/)
[MongoDB](https://www.mongodb.com)
and native [python](https://www.python.org) 

## Premise

All test will start with the exact same data structure
and number of rows/documents.

## Postgres

Our postgres test will use the
[tablefunc](https://www.postgresql.org/docs/9.2/static/tablefunc.html)
module via the [django-pivot](https://github.com/martsberger/django-pivot)
app.

## MongoDB

Our mongodb test will use
[group aggregation](http://docs.mongodb.org/manual/reference/aggregation/group/)

## Python

And for our native python test we'll use
[pandas](http://pandas.pydata.org/)
