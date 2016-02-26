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

```t = tweets.find({"keywords" : {"$in" : ["yellow"]}})```

To return all tweets containing the word "yellow" or "jackets":

```t = tweets.find({"keywords" : {"$in" : ["yellow", "jackets"]}})```

Once you find your set of tweets, to iterate through the cursor:

<pre><code>for tweet in t:
  print(tweet)</code></pre>

## Tweet Entities

'text': original text of tweet (str format)

'author_id': author's id in twitter's system (str format)

'author_name': author's name (str format)

'author_followers_count': how many people follow the author (int format)

'timestamp': when is the tweet created (int format) // we started to use new crawler since 1456524600

'lon': longitude of tweet (int format)

'lat': latitude of tweet (int format)

'words': all words in text (list of str)

'keywords': keywords in text (list of str)

'hashtags': hashtags in text (list of str)

'mentions_id': ids of people being mentioned in tweet (list of str)

'mentions_name': names of people being mentioned in tweet (list of str)

'urls': urls in text (list of str)
