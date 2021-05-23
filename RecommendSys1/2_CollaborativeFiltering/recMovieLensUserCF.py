import random
import math
import json
import os

class UserCFRec:
    def __init__(self,datafile):
        self.datafile = datafile
        self.data = self.loadData()
        self.trainData, self.testData = self.splitData(3,2021)
        self.users_sim = self.userSimilarityBest()

    def loadData(self):
        print('load data ...')
        data = []
        for line in open(self.datafile):
            userid,itemid,record,_ = line.split('::')
            data.append((userid,itemid,int(record)))
        return data

    def splitData(self,k,seed,M=8):
        print('split dataset into trainset and testset. 1/{} testset.'.format(M))
        train,test = {},{}
        random.seed(seed)
        for user,item,record in self.data:
            if random.randint(0,M) == k:
                test.setdefault(user,{})
                test[user][item] = record
            else:
                train.setdefault(user,{})
                train[user][item] = record
        return train,test

    ## 计算用户相似度优化2：针对hot打压的优化
    def userSimilarityBest(self):
        print('calculating similarity between every two users')
        if (os.path.exists('../data/ml-1m/user_sim.json')):
            print('user similarity file loading...')
            W = json.load(open('../data/ml-1m/user_sim.json','r'))
        else:
            ## 构建倒排表
            item_users = dict()
            for u, items in self.trainData.items():
                for i in items.keys():
                    item_users.setdefault(i,set())
                    if self.trainData[u][i] > 0:
                        item_users[i].add(u)
            ## 构建用户相似矩阵
            C = dict() ## 分子
            N = dict() ## 分母
            for i, users in item_users.items():
                for u in users:
                    N.setdefault(u,0)
                    N[u] += 1

                    C.setdefault(u,{})
                    for v in users:
                        C[u].setdefault(v,0)
                        if u == v:
                            continue
                        C[u][v] += 1/math.log(1+len(users)) ## keypoint
            ## 计算用户相似度
            W = dict()
            for u, related_users in C.items():
                W.setdefault(u,{})
                for v, cnt in related_users.items():
                    if u == v:
                        continue
                    W[u].setdefault(v,0)
                    W[u][v] = cnt / math.sqrt(N[u] * N[v])
            json.dump(W,open('../data/ml-1m/user_sim.json','w'))
        return W

    ## 推荐, topk user, topn item
    def recommend(self, user, k=8, n=40):
        result = dict()
        have_score_items = self.trainData.get(user,{})
        for related_users,simi_score in sorted(self.users_sim[user].items(),key=lambda x:x[1], reverse=True)[0:k]:
            for related_user,related_rating in self.trainData[related_users].items():
                if related_user in have_score_items:
                    continue
                result.setdefault(related_user,0)
                result[related_user] += simi_score * related_rating
        return dict(sorted(result.items(), key=lambda x:x[1], reverse=True)[0:n])

    ## 评估
    def precision(self, k=8, n=10):
        print('start calculating precision')
        hit = 0
        tot = 0
        for user in self.trainData.keys():
            tru = self.testData.get(user,{})
            result = self.recommend(user, k=k, n=n)
            for item,rate in result.items():
                if item in tru:
                    hit += 1
            tot += n
        return hit / (tot * 1.0)


if __name__ == '__main__':
    cf = UserCFRec('../data/ml-1m/ratings.dat')
    result = cf.recommend('1')
    print('user 1 recommend result is {}'.format(result))
    precision = cf.precision()
    print('precision is {}'.format(precision))