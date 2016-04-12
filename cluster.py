from dbco import *
from igraph import *
import pymongo
import time

# use create_index to timestamp on database before matching
# $unwind keywords
# $group by keywords
#     {'_id': 'obama', 'tweetIDs':['101','203','401'], 'count': 20}
# then build a dictionary containing
#     {'key': '101, 203', 'value': 1}
# so now we have edges

def buildGraph():
    graph = Graph()
    match1 = {'$match':{'timestamp':{'$gte':time.time()-3600*6}, 'author_followers_count':{'$gte':5000}}}
    #samples = list(db.tweet.aggregate([match1]))
    #graph.add_vertices(len(samples))
    #print ("#Nodes: ", len(samples))
    unwind = {'$unwind': '$keywords'}
    group = {'$group':{'_id':'$keywords', 'tweet_guids':{'$push':'$guid'}, 'count':{'$sum':1}}}
    match2 = {'$match':{'count':{'$gte':100}}}
    pipeline = [match1, unwind, group, match2]
    kwGroup = list(db.tweet.aggregate(pipeline))
    edgeDict = dict()
    # maybe if we do add_vertex instead of add_vertices, we don't need the referDict
    referDict = dict()
    counter = 0
    for kwGroupElem in kwGroup:
        for i in range(len(kwGroupElem['tweet_guids'])-1):
            if (kwGroupElem['tweet_guids'][i] not in referDict):
                referDict[kwGroupElem['tweet_guids'][i]] = counter
                counter += 1
            for j in range(i+1, len(kwGroupElem['tweet_guids'])):
                if (kwGroupElem['tweet_guids'][j] not in referDict):
                    referDict[kwGroupElem['tweet_guids'][j]] = counter
                    counter += 1
                key = kwGroupElem['tweet_guids'][i] + " " + kwGroupElem['tweet_guids'][j]
                if (key not in edgeDict):
                    edgeDict[key] = 1
                else:
                    edgeDict[key] += 1
    edgeList = list()
    edgeListToGraph = list()
    for k,v in edgeDict.iteritems():
        if v > 2:
            key = k.split()
            edgeList.append({'source': key[0], 'target': key[1], 'value': v})
            edgeListToGraph.append((referDict[key[0]], referDict[key[1]]))
    graph.add_vertices(counter)
    graph.add_edges(edgeListToGraph)
    infomap = graph.community_infomap()
    print "#Samples: ", counter
    print
    print edgeList
    print
    print infomap

buildGraph()