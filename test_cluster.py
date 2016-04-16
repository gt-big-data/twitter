from dbco import *
from cluster import *
import pymongo
import time

def test(followers, hours):
    t = time.time()
    clusters = get_clusters(followers, hours)
    runtime = time.time() - t
    print "Running time: ", runtime, " seconds"
    for cluster in clusters:
        print "-----------------------------------------------"
        for tweet in cluster:
            print "-> ", tweet['text']

test(10000, 3)