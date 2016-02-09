# Twitter

Using Retina News' database of tweets to run various analysis.

## Requirements

### Python

[Download Python 3](https://www.python.org/downloads/)

### PyMongo

```pip install pymongo```

## Accessing Database of tweets

Open a new python file and start with

<pre><code>from pymongo import MongoClient

client = MongoClient('mongodb://db.retinanews.net')
db = client.big_data
tweets = db.tweet</code></pre>

