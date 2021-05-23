import math

class ItemCF:
    def __init__(self):
        self.user_score_dict = self.initUserScore()
        # self.item_sim = self.itemSimilarity()
        self.item_sim = self.itemSimilarityBest()

    def initUserScore(self):
        user_score_dict = {'A':{'a':3.0, 'b':4.0, 'c':0.0, 'd':3.5, 'e':0.0},
                            'B':{'a':4.0, 'b':0.0, 'c':4.5, 'd':0.0, 'e':3.5},
                            'C':{'a':0.0, 'b':3.5, 'c':0.0, 'd':0.0, 'e':3.0},
                            'D':{'a':0.0, 'b':4.0, 'c':0.0, 'd':3.5, 'e':3.0}}
        return user_score_dict

    ## 计算item之间相似度
    def itemSimilarity(self):
        ## 同现矩阵
        item_user_count = dict()  ## {item:cnt}
        count = dict()  ## {item1:{item2:cnt}}
        for user,item in self.user_score_dict.items():
            for i in item.keys():
                item_user_count.setdefault(i,0)
                if self.user_score_dict[user][i] > 0.0:
                    item_user_count[i] += 1

                for j in item.keys():
                    count.setdefault(i,{}).setdefault(j,0)
                    if (i!=j and self.user_score_dict[user][i]>0.0 and self.user_score_dict[user][j]>0.0):
                        count[i][j] += 1
        ## 相似矩阵
        itemSim = dict()
        for i,related_items in count.items():
            itemSim.setdefault(i,dict())
            for j,cnt in related_items.items():
                itemSim[i].setdefault(j,0)
                itemSim[i][j] = cnt / item_user_count[i]  ##
        return itemSim

    ## 计算item之间相似度优化：针对hot打压的优化
    def itemSimilarityBest(self):
        ## 同现矩阵
        item_user_count = dict()  ## {item:cnt}
        count = dict()  ## {item1:{item2:cnt}}
        for user,item in self.user_score_dict.items():
            for i in item.keys():
                item_user_count.setdefault(i,0)
                if self.user_score_dict[user][i] > 0.0:
                    item_user_count[i] += 1

                for j in item.keys():
                    count.setdefault(i,{}).setdefault(j,0)
                    if (i!=j and self.user_score_dict[user][i]>0.0 and self.user_score_dict[user][j]>0.0):
                        count[i][j] += 1
        ## 相似矩阵
        itemSim = dict()
        for i,related_items in count.items():
            itemSim.setdefault(i,dict())
            for j,cnt in related_items.items():
                itemSim[i].setdefault(j,0)
                itemSim[i][j] = cnt / math.sqrt(item_user_count[i] * item_user_count[j])  ##
        return itemSim

    def preUserItemScore(self,userA,item):
        score = 0.0
        for related_item in self.item_sim[item].keys():
            if related_item != item:
                score += (self.item_sim[item][related_item] * self.user_score_dict[userA][related_item]) ##
        return score

    def recommend(self,userA):
        user_item_score_dict = dict()
        for item in self.user_score_dict[userA].keys():
            if self.user_score_dict[userA][item] <= 0:
                user_item_score_dict[item] = self.preUserItemScore(userA,item)
        return user_item_score_dict


if __name__ == '__main__':
    icf = ItemCF()
    print(icf.recommend('C'))