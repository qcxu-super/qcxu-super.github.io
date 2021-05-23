import random
import math
import json
import os

class ItemCFRec:
    def __init__(self,datafile):
        self.datafile = datafile
        self.data = self.loadData()
        self.trainData, self.testData = self.splitData(3,2021)
        self.items_sim = self.itemSimilarityBest()

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


    ## 计算item之间相似度优化：针对hot打压的优化
    def itemSimilarityBest(self):
        print('calculating similarity between every two items')
        if (os.path.exists('../data/ml-1m/item_sim.json')):
            print('user similarity file loading...')
            itemSim = json.load(open('../data/ml-1m/item_sim.json','r'))
        else:
            ## 同现矩阵
            item_user_count = dict()  ## {item:cnt}
            count = dict()  ## {item1:{item2:cnt}}
            for user,item in self.trainData.items():
                for i in item.keys():
                    item_user_count.setdefault(i,0)
                    if self.trainData[user][i] > 0.0:
                        item_user_count[i] += 1

                    for j in item.keys():
                        count.setdefault(i,{}).setdefault(j,0)
                        if (i!=j and self.trainData[user][i]>0.0 and self.trainData[user][j]>0.0):
                            count[i][j] += 1
            ## 相似矩阵
            itemSim = dict()
            for i,related_items in count.items():
                itemSim.setdefault(i,dict())
                for j,cnt in related_items.items():
                    itemSim[i].setdefault(j,0)
                    itemSim[i][j] = cnt / math.sqrt(item_user_count[i] * item_user_count[j])  ##
            json.dump(itemSim, open('../data/ml-1m/item_sim.json','w'))
        return itemSim

    ## 推荐, topk item, topn return
    def recommend(self, user, k=8, n=40):
        result = dict()
        u_items = self.trainData.get(user,{})
        for u,rating in u_items.items():
            for j,wj in sorted(self.items_sim[u].items(), key=lambda x: x[1], reverse=True)[0:k]:
                if j in u_items:
                    continue
                result.setdefault(j,0)
                result[j] += rating * wj
        return dict(sorted(result.items(),key=lambda x: x[1], reverse=True)[0:n])

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
    cf = ItemCFRec('../data/ml-1m/ratings.dat')
    result = cf.recommend('1')
    print('user 1 recommend result is {}'.format(result))
    precision = cf.precision()
    print('precision is {}'.format(precision))
