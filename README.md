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
[group aggregation](http://docs.mongodb.org/manual/reference/aggregation/group/) and [djongo](https://github.com/nesdis/djongo)

[ref](https://stackoverflow.com/a/17401008)

### Python

(*coming soon*) And for our native python test we'll use
[pandas](http://pandas.pydata.org/)

## The Data

This is just a very basic test with a simplest pivot table.
All test will start with the exact same data structure (example below) and number of rows (or documents in the case of MongoDB). This test will use **1 Million** rows for input and expect **1000** output rows. Some filtering tests may bring the output list down to 100 or even 10.

### Stored data: a list of course/student/score pairings

Course | Student | Score
------ | ------- | -----
A01    | Gary    | 20
A01    | Cindy   | 21
...    | ...     | ...

### Desired output: each students scores by course

Student | A01 Score | B01 Score
------- | --------- | ---------
Gary    | 20        | 19
Cindy   | 21        | 31
...     | ...       | ...

#### MongoDB Format

Standard Postgres and SQL data can be represented using the tables above, but MongoDB needs to be represented with json.

So, stored data will look something like this:

```javascript
[
    { 'course_name': 'A01', 'student_name': 'Gary', 'score': 20 },
    { 'course_name': 'A01', 'student_name': 'Cindy', 'score': 21 },
    ...
]
```

The output should look more like:
```javascript
[
    {
        '_id': 'Gary',
        'scores': [
            { 'course_name': 'A01', 'score': 20 },
            { 'course_name': 'B01', 'score': 19 },
            ...
        ]
    },
    {
        '_id': 'Cindy',
        'scores': [
            { 'course_name': 'A01', 'score': 20 },
            { 'course_name': 'B01', 'score': 19 },
            ...
        ]
    },
    ...
]
```

## Performance Results

Loading fixtures in the standard django way from json files resulted in some crazy load times for MongoDB. After using `mongodump` and `mongorestore`, I was able to get this down from 9 hours to 7 seconds. Most applications won't have to worry about this, but those using ETL actions might need to look at better ways to load data periodically.

```
Elapased Time: 32778.961s
```

Fixture loading was slow for PG too, but not to the same extent. This could probably be improved by using `pg_dump` instead of standard fixtures.

### Here are the results:

```
$ dj test
Creating test database for alias 'default'...
Creating test database for alias 'mongo'...
System check identified no issues (0 silenced).

###
Mongo Test
###

loading fixture
done loading fixture
Elapased Time: 9.159s

---
Testing on 1040000 records
---
Filtered Test (10 students, 5 courses)
Elapased Time: 0.425s
---
Filtered Test (100 students, 10 courses)
Elapased Time: 0.448s
---
Filtered Test (1000 students, 20 courses)
Elapased Time: 0.486s
.
###
Postgres Test
###

loading fixture
done loading fixture
Elapased Time: 877.260s

---
Testing on 1050400 records
---
Filtered Test (10 students, 5 courses)
Elapased Time: 0.567s
---
Filtered Test (100 students, 10 courses)
Elapased Time: 0.560s
---
Filtered Test (1000 students, 20 courses)
Elapased Time: 0.581s
.
----------------------------------------------------------------------
Ran 2 tests in 905.891s

OK
Destroying test database for alias 'default'...
Destroying test database for alias 'mongo'...
```
