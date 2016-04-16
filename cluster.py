from dbco import *
from igraph import *
import pymongo
import time

# @param min_followers_count: if a tweet's author has less followers than min_followers_count, we ignore that tweet
# @param num_of_hours: select data in a time range between num_of_hours before to now
# @return clusters: a list that contains tweet clusters
# @note get_clusters(5000,1) takes about 1 second, get_clusters(10000,3) takes about 4 seconds, get_clusters(5000,6) takes about 80 seconds

def get_clusters(followers=3000, hours=1):
    # use create_index to timestamp on database before matching
    # $unwind keywords
    # $group by keywords
    #     {'_id': 'obama', 'tweet':[{xxx},{yyy},{zzz}], 'count': 20}
    # then build a dictionary containing
    #     {'key': ({xxx}, {yyy}), 'value': 1}
    # so now we have edges
    graph = Graph()
    match1 = {'$match':{'timestamp':{'$gte':time.time()-3600*hours}, 'author_followers_count':{'$gte':followers}}}
    unwind = {'$unwind': '$keywords'}
    group = {'$group':{'_id':'$keywords', 'tweet':{'$push':'$$ROOT'}, 'count':{'$sum':1}}}
    match2 = {'$match':{'count':{'$gte':100}}}
    pipeline = [match1, unwind, group, match2]
    kwGroup = list(db.tweet.aggregate(pipeline))
    edgeDict = dict()
    referDict = dict()
    referBackDict = dict()
    counter = 0
    for kwGroupElem in kwGroup:
        for i in range(len(kwGroupElem['tweet'])-1):
            if (kwGroupElem['tweet'][i]['guid'] not in referDict):
                referDict[kwGroupElem['tweet'][i]['guid']] = counter
                referBackDict[counter] = kwGroupElem['tweet'][i]
                counter += 1
                for j in range(i+1, len(kwGroupElem['tweet'])):
                    if (kwGroupElem['tweet'][j]['guid'] not in referDict):
                        referDict[kwGroupElem['tweet'][j]['guid']] = counter
                        referBackDict[counter] = kwGroupElem['tweet'][j]
                        counter += 1
                    key = (kwGroupElem['tweet'][i]['guid'], kwGroupElem['tweet'][j]['guid'])
                    edgeDict[key] = 1
                continue
            for j in range(i+1, len(kwGroupElem['tweet'])):
                if (kwGroupElem['tweet'][j]['guid'] not in referDict):
                    referDict[kwGroupElem['tweet'][j]['guid']] = counter
                    referBackDict[counter] = kwGroupElem['tweet'][j]
                    counter += 1
                    key = (kwGroupElem['tweet'][i]['guid'], kwGroupElem['tweet'][j]['guid'])
                    edgeDict[key] = 1
                    continue
                key = (kwGroupElem['tweet'][i]['guid'], kwGroupElem['tweet'][j]['guid'])
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
    for cluster in infomap:
        if len(cluster) > 1:
            cluster_tweet = list()
            for elem in cluster:
                cluster_tweet.append(referBackDict[elem])
            clusters.append(cluster_tweet)
    return clusters