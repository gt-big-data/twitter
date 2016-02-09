# Twitter

Using Retina News' database of tweets to run various analysis.

## Requirements

### Python

[Download Python 2](https://www.python.org/downloads/)

### PyMongo

Run the following command in your terminal window, after downloading Python:

```pip install pymongo```

## Accessing Database of Tweets

Open a new python file and start with

<pre><code>from pymongo import MongoClient

client = MongoClient('mongodb://db.retinanews.net')
db = client.big_data
tweets = db.tweet</code></pre>

## Querying Tweets

Examine the [MongoDB documentation](https://docs.mongodb.org/getting-started/python/query/)

To return a random tweet:

```t = tweets.find_one()```

To return all tweets containing the word "yellow":

```t = tweets.find({"words" : {"$in" : ["yellow"]}})```

To return all tweets containing the word "yellow" or "jackets":

```t = tweets.find({"words" : {"$in" : ["yellow", "jackets"]}})```

Once you find your set of tweets, to iterate through the cursor:

<pre><code>for tweet in t:
  print(tweet)</code></pre>
