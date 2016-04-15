from dbco import *
from igraph import *
import pymongo
import time

# @param min_followers_count: if a tweet's author has less followers than min_followers_count, we ignore that tweet
# @param num_of_hours: select data in a time range between num_of_hours before to now
# @return clusters: a list that contains tweet clusters, GUIDs are saved in clusters
# @note get_clusters(5000,1) takes about 1 second, get_clusters(10000,3) takes about 4 seconds, get_clusters(5000,6) takes about 80 seconds

def get_clusters(followers=3000, hours=1):
    # use create_index to timestamp on database before matching
    # $unwind keywords
    # $group by keywords
    #     {'_id': 'obama', 'tweetIDs':['101','203','401'], 'count': 20}
    # then build a dictionary containing
    #     {'key': '101, 203', 'value': 1}
    # so now we have edges
    graph = Graph()
    match1 = {'$match':{'timestamp':{'$gte':time.time()-3600*hours}, 'author_followers_count':{'$gte':followers}}}
    unwind = {'$unwind': '$keywords'}
    group = {'$group':{'_id':'$keywords', 'tweet_guids':{'$push':'$guid'}, 'count':{'$sum':1}}}
    match2 = {'$match':{'count':{'$gte':100}}}
    pipeline = [match1, unwind, group, match2]
    kwGroup = list(db.tweet.aggregate(pipeline))
    edgeDict = dict()
    referDict = dict()
    referBackDict = dict()
    counter = 0
    for kwGroupElem in kwGroup:
        for i in range(len(kwGroupElem['tweet_guids'])-1):
            if (kwGroupElem['tweet_guids'][i] not in referDict):
                referDict[kwGroupElem['tweet_guids'][i]] = counter
                referBackDict[counter] = kwGroupElem['tweet_guids'][i]
                counter += 1
                for j in range(i+1, len(kwGroupElem['tweet_guids'])):
                    if (kwGroupElem['tweet_guids'][j] not in referDict):
                        referDict[kwGroupElem['tweet_guids'][j]] = counter
                        referBackDict[counter] = kwGroupElem['tweet_guids'][j]
                        counter += 1
                    key = (kwGroupElem['tweet_guids'][i], kwGroupElem['tweet_guids'][j])
                    edgeDict[key] = 1
                continue
            for j in range(i+1, len(kwGroupElem['tweet_guids'])):
                if (kwGroupElem['tweet_guids'][j] not in referDict):
                    referDict[kwGroupElem['tweet_guids'][j]] = counter
                    referBackDict[counter] = kwGroupElem['tweet_guids'][j]
                    counter += 1
                    key = (kwGroupElem['tweet_guids'][i], kwGroupElem['tweet_guids'][j])
                    edgeDict[key] = 1
                    continue
                key = (kwGroupElem['tweet_guids'][i], kwGroupElem['tweet_guids'][j])
                if (key in edgeDict):
                    edgeDict[key] += 1
                elif ((key[1], key[0]) in edgeDict):
                    edgeDict[(key[1], key[0])] += 1
                else:
                    edgeDict[key] = 1
    edgeListToGraph = list()
    for k,v in edgeDict.iteritems():
        if v > 3:
            edgeListToGraph.append((referDict[k[0]], referDict[k[1]]))
    graph.add_vertices(counter)
    graph.add_edges(edgeListToGraph)
    infomap = graph.community_infomap()
    clusters = list()
    for info in infomap:
        if len(info) > 1:
            info_guid = list()
            for elem in info:
                info_guid.append(referBackDict[elem])
            clusters.append(info_guid)
    return clusters