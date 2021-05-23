import math

class UserCF:
    def __init__(self):
        self.user_score_dict = self.initUserScore()
        # self.users_sim = self.userSimilarity()
        # self.users_sim = self.userSimilarityBetter()
        self.users_sim = self.userSimilarityBest()

    def initUserScore(self):
        user_score_dict = {'A':{'a':3.0, 'b':4.0, 'c':0.0, 'd':3.5, 'e':0.0},
                            'B':{'a':4.0, 'b':0.0, 'c':4.5, 'd':0.0, 'e':3.5},
                            'C':{'a':0.0, 'b':3.5, 'c':0.0, 'd':0.0, 'e':3.0},
                            'D':{'a':0.0, 'b':4.0, 'c':0.0, 'd':3.5, 'e':3.0}}
        return user_score_dict

    ## 计算用户之间的相似度
    def userSimilarity(self):
        W = dict()
        for u in self.user_score_dict.keys():  # foreach user
            W.setdefault(u,{})
            for v in self.user_score_dict.keys(): # foreach user
                if u == v:
                    continue
                u_set = set([k for k in self.user_score_dict[u].keys() if self.user_score_dict[u][k]>0.0])
                v_set = set([k for k in self.user_score_dict[v].keys() if self.user_score_dict[v][k]>0.0])
                W[u][v] = float(len(u_set & v_set)) / math.sqrt(len(u_set) * len(v_set))
        return W

    ## 计算用户相似度优化1：针对计算时间复杂度的优化
    def userSimilarityBetter(self):
        ## 构建倒排表
        item_users = dict()
        for u, items in self.user_score_dict.items():
            for i in items.keys():
                item_users.setdefault(i,set())
                if self.user_score_dict[u][i] > 0:
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
                    C[u][v] += 1  ## user u,v action in common
        ## 计算用户相似度
        W = dict()
        for u, related_users in C.items():
            W.setdefault(u,{})
            for v, cnt in related_users.items():
                if u == v:
                    continue
                W[u].setdefault(v,0)
                W[u][v] = cnt / math.sqrt(N[u] * N[v])
        return W

    ## 计算用户相似度优化2：针对hot打压的优化
    def userSimilarityBest(self):
        ## 构建倒排表
        item_users = dict()
        for u, items in self.user_score_dict.items():
            for i in items.keys():
                item_users.setdefault(i,set())
                if self.user_score_dict[u][i] > 0:
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
        return W

    ## 计算用户对item的评分
    def predictUserItemScore(self, userA, item):
        score = 0.0
        for user in self.users_sim[userA].keys(): # foreach similar user
            if user != userA:
                score += self.users_sim[userA][user] * self.user_score_dict[user][item]
        return score

    ## 推荐
    def recommend(self, userA):
        user_item_score_dict = dict()
        for item in self.user_score_dict[userA].keys():
            if self.user_score_dict[userA][item] <= 0:
                user_item_score_dict[item] = self.predictUserItemScore(userA, item)
        return user_item_score_dict


if __name__ == '__main__':
    ucf = UserCF()
    print(ucf.recommend('C'))