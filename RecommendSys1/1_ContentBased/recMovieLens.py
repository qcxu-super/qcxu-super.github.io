import pandas as pd
import json
import math
import numpy as np
import random

class DataProcessing:
    def __init__(self):
        pass

    ## 数据格式转换
    def process(self):
        print('user data: dat to csv...')
        self.process_user_data()
        print('movie data: dat to csv ...')
        self.process_movies_data()
        print('rating data: dat to csv ...')
        self.process_rating_data()
        print('Success')

    def process_user_data(self, file='../data/ml-1m/users.dat'):
        fp = pd.read_table(file, sep='::', engine='python', names=['UserID','Gender','Age','Occupation','Zip-code'])
        fp.to_csv('../data/ml-1m/users.csv', index=False)

    def process_rating_data(self, file='../data/ml-1m/ratings.dat'):
        fp = pd.read_table(file, sep='::', engine='python', names=['UserID','MovieID','Rating','TimeStamp'])
        fp.to_csv('../data/ml-1m/ratings.csv', index=False)

    def process_movies_data(self, file='../data/ml-1m/movies.dat'):
        fp = pd.read_table(file, sep='::', engine='python', names=['MovieID','Title','Genres'])
        fp.to_csv('../data/ml-1m/movies.csv', index=False)

    ## 计算物品的特征信息矩阵。各物品都属于哪些类别
    def prepare_item_profile(self, file='../data/ml-1m/movies.csv'):
        items = pd.read_csv(file)
        item_ids = set(items['MovieID'].values) # all items

        self.item_dict = {} # {MovieId: [genres]}
        genres_all = list() # all genres
        for item in item_ids:
            genres = items.loc[items['MovieID']==item, 'Genres'].values[0].split('|')
            self.item_dict.setdefault(item,[]).extend(genres)
            genres_all.extend(genres)
            self.genres_all = set(genres_all)
        self.genres_all_list = list(self.genres_all)

        self.item_matrix = {} # {MovieId: [one-hot for genres]}
        for item in self.item_dict.keys(): # key: MovieID
            self.item_matrix[str(item)] = [0] * len(set(self.genres_all))
            for genre in self.item_dict[item]: # value: [genres]
                index = self.genres_all_list.index(genre)
                self.item_matrix[str(item)][index] = 1
        json.dump(self.item_matrix, open('../data/ml-1m/item_profile.json','w'))

        print('Success. Item Matrix. Save to path {}'.format('../data/ml-1m/item_profile.json'))

    ## 计算用户的偏好矩阵。用户对各类别的偏好
    def prepare_user_profile(self, file='../data/ml-1m/ratings.csv'):
        users = pd.read_csv(file)
        user_ids = set(users['UserID'].values)

        users_rating_dict = {} # {user1: {item1:rate1, item2:rate2, ...}, user2:{...}, ...}
        for user in user_ids:
            users_rating_dict.setdefault(str(user),{})
        with open(file,'r') as fr:
            for line in fr.readlines():
                if not line.startswith('UserID'):
                    (user,item,rate) = line.split(',')[:3]
                    users_rating_dict[user][item] = int(rate)

        self.user_matrix = {} # {user1: [rate11,rate12,...], user2: [rate21,rate22,...], ...}
        for user in users_rating_dict.keys():
            item_rating_dict = users_rating_dict[user] # users_rating_dict[user]={item1:rate1, item2:rate2, ...}
            score_list = item_rating_dict.values() # [rate1,rate2,...]
            avg = sum(score_list)/len(score_list)
            self.user_matrix[user] = []
            for genre in self.genres_all_list: # for each genres
                score_all = 0.0
                score_len = 0
                for item in item_rating_dict.keys(): # [item1,item2,...], for each item user rates
                    if genre in self.item_dict[int(item)]: # genres of item == current genres
                        score_all += (item_rating_dict[item]-avg) ##
                        score_len += 1
                if score_len == 0:
                    self.user_matrix[user].append(0.0)
                else:
                    self.user_matrix[user].append(score_all/score_len)
        json.dump(self.user_matrix, open('../data/ml-1m/user_profile.json','w'))
        print('Success. User Matrix. Save to path {}'.format('../data/ml-1m/user_profile.json'))

class CBRecommend:
    ## topK推荐。加载物品的特征信息矩阵，用户的偏好矩阵
    def __init__(self, k):
        self.k = k
        self.item_profile = json.load(open('../data/ml-1m/item_profile.json','r'))
        self.user_profile = json.load(open('../data/ml-1m/user_profile.json','r'))

    ## 获取用户未进行评分的item列表
    def get_none_score_item(self, user):
        items = pd.read_csv('../data/ml-1m/movies.csv')['MovieID'].values
        data = pd.read_csv('../data/ml-1m/ratings.csv')
        have_score_items = data.loc[data['UserID']==user, 'MovieID'].values
        none_score_items = set(items)-set(have_score_items)
        return none_score_items

    ## 获取用户对item的喜好程度
    def cosUI(self, user, item):
        UIa = sum(np.array(self.user_profile[str(user)]) * np.array(self.item_profile[str(item)]))
        Ua = math.sqrt(sum([math.pow(one,2) for one in self.user_profile[str(user)]]))
        Ia = math.sqrt(sum([math.pow(one,2) for one in self.item_profile[str(item)]]))
        return UIa / (Ua * Ia)

    ## 为用户进行推荐
    def recommend(self, user):
        user_result = {}
        item_list = self.get_none_score_item(user)
        for item in item_list:
            user_result[item] = self.cosUI(user, item)
        if self.k is None:
            result = sorted(user_result.items(), key=lambda k: k[1], reverse=True)
        else:
            result = sorted(user_result.items(), key=lambda k: k[1], reverse=True)[:self.k]
        print(result)

    ## 评估
    def evaluate(self):
        evas = []
        data = pd.read_csv('../data/ml-1m/ratings.csv')
        for user in random.sample([one for one in range(1,6040)],20): # random sample 20 users
            have_score_items = data.loc[data['UserID']==user,'MovieID'].values
            items = pd.read_csv('../data/ml-1m/movies.csv')['MovieID'].values

            user_result = {} # {item1:score1, item2:score2, ...}
            for item in items:
                user_result[item] = self.cosUI(user,item)
            
            result = sorted(user_result.items(), key=lambda k: k[1], reverse=True)[:len(have_score_items)]
            rec_items = [one[0] for one in result]
            eva = len(set(rec_items) & set(have_score_items)) / len(have_score_items)
            evas.append(eva)
        return sum(evas)/len(evas) # avg


if __name__ == '__main__':
    dp = DataProcessing()
    dp.process()
    dp.prepare_item_profile()
    dp.prepare_user_profile()

    cb = CBRecommend(k=10)
    cb.recommend(user=1)
    evares = cb.evaluate()
    print(evares)