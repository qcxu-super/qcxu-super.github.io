
# 0. CF

协同过滤，基于近邻的推荐算法，主要有以下两类：

- 基于用户的协同过滤(User-CF)
- 基于物品的协同过滤(Item-CF)

举个例子：

不知道哪个电影是自己喜欢的或评分高的，这时通常会问“跟自己品味差不多”的朋友，看他有什么电影推荐。

# 1. User-CF

## 1.1 算法思路

给用户推荐：“和他兴趣相投的其他用户”喜欢的物品。所以，先找到“相似用户”，再找到“他们喜欢的物品”。

那怎么衡量用户的相似性呢？通过`不同用户`对`相同物品`的评分或偏好程度！

那怎么衡量用户可能有喜欢的该物品？这取决于相似用户有多喜欢该物品！

![image](https://gitee.com/journey7878/img-bed/raw/master/RecommendSys1/picUserCF1.png)

举个例子：

- 用户A和用户C同时喜欢电影A和电影C
- 用户C还喜欢电影D
- 所以，把用户A没有表达喜好的电影D推荐给用户A

## 1.2 算法实现

### 1 实现步骤

step1 计算得到用户C的相似用户

step2 找到这些相似用户喜欢、但用户C没有进行过评分的物品，并推荐给用户C

### 2 举例

#### step0 构建用户物品评分表

| 姓名        | 物品a  | 物品b | 物品c | 物品d | 物品e
| ------------- |:-----|:-----|:-----|
| A | 3.0 | 4.0 | 0 | 3.5 | 0
| B | 4.0 | 0   | 4.5 | 0 | 3.5
| C | 0 | 3.5 | 0 | 0 | 3
| D | 0 | 4 |0 | 3.5 | 3


#### step1 计算用户相似度

根据用户历史行为，可以用余弦相似度衡量用户之间的相似度。

![image](https://gitee.com/journey7878/img-bed/raw/master/RecommendSys1/picUserCF2.png)

其中，
- N(u): 用户u有过评分的物品集合
- N(v): 用户v有过评分的物品集合

所以，结合上表，用户C跟其他三个用户的相似度如下：

![image](https://gitee.com/journey7878/img-bed/raw/master/RecommendSys1/picUserCF3.png)

![image](https://gitee.com/journey7878/img-bed/raw/master/RecommendSys1/picUserCF4.png)

![image](https://gitee.com/journey7878/img-bed/raw/master/RecommendSys1/picUserCF5.png)

从计算结果看，用户D和用户C相似度最大。

（Q：感觉这里不是很合理。。如果用户A和用户B都只对物品abc评分，一个全部都是好评，一个全部都是差评，那按这个公式算，这俩用户相似度为1？？）


#### step2 计算推荐结果

根据用户的相似度，以及相似用户对不同物品的偏好，可以推测当前用户对物品的偏好。

![image](https://gitee.com/journey7878/img-bed/raw/master/RecommendSys1/picUserCF6.png)

```
p(C,a) = W_{CA} × 3.0 + W_{CB} × 4.0 + W_{CD} × 3.5 = 2.858
p(C,c) = W_{CA} × 0.0 + W_{CB} × 4.5 + W_{CD} × 0.0 = 1.837
p(C,d) = W_{CA} × 3.5 + W_{CB} × 0.0 + W_{CD} × 3.0 = 4.287
```

所以，在用户C没有评分的物品中，倒序排序为：d,a,c。从而推荐topK给用户C。


[User-Based算法原理](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/RecommendSys1/2_CollaborativeFiltering/userBased.py)


## 1.3 算法优化1

针对计算时间复杂度的优化。

上述代码最大的问题在于，如果有N个用户，则时间复杂度是O(N^2)。实际情况中，很多用户是没有交集的，也就是说，没有对同一物品产生过行为。所以很多分子都是0，这种计算是不必要的。

所以可以，先计算 `N(u) ∩ N(v) ≠ 0` 的用户对 (u,v)，然后对其除以分母，就可以得到用户u,v的相似度。


### 1 实现步骤

#### step1 建立倒排表

建立物品到用户的倒排表T，表示该物品被哪些用户产生过行为


#### step2 建立用户相似矩阵 W (余弦相似度分子部分)，计算用户相似度

- 在倒排表T中，对于物品i，设其对应的用户为j,k
- 在用户相似矩阵W中，更新对应元素值：W[j][k]+=1, W[k][j]+=1
- W/分母，得到两个用户的兴趣相似度

#### step3 计算推荐结果

同baseline版本的step2


### 2 举例

#### step1 建立倒排表

由用户的评分数据，得到每个物品被哪些用户评价过。

![image](https://gitee.com/journey7878/img-bed/raw/master/RecommendSys1/picUserCF7.png)

比如说，在物品b和物品e中，都同时出现了用户C和用户D

#### step2 建立用户相似矩阵 W (余弦相似度分子部分)


两个用户共同点评的物品数越多，那么他们越相似。所以统计，两两用户的共同点评数，即为用户相似矩阵。

比如说，W[C][D]=W[D][C]=2，用户C和用户D共同点评的物品有2个。

![image](https://gitee.com/journey7878/img-bed/raw/master/RecommendSys1/picUserCF8.png)


以用户C为例，C∩A=1，C∩B=1，C∩D=2

![image](https://gitee.com/journey7878/img-bed/raw/master/RecommendSys1/picUserCF9.png)

#### step3 计算推荐结果

![image](https://gitee.com/journey7878/img-bed/raw/master/RecommendSys1/picUserCF10.png)

其中，
- P(u,i), 用户u对物品i的感兴趣程度
- S(u,K), 和用户u最相似的K个用户
- N(i), 对物品i有过行为的用户集合
- S(u,K) ∩ N(i), 对物品i有过行为的K个最相似用户
- W_{uv}, 用户u和用户v的相似度
- r_{vi}, 用户v对物品i的喜好程度

```
p(C,a) = W_{CA} × 3.0 + W_{CB} × 4.0 + W_{CD} × 3.5 = 2.858
p(C,c) = W_{CA} × 0.0 + W_{CB} × 4.5 + W_{CD} × 0.0 = 1.837
p(C,d) = W_{CA} × 3.5 + W_{CB} × 0.0 + W_{CD} × 3.0 = 4.287
```


[User-Based算法原理 (计算用户相似度优化1) - userSimilarityBetter](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/RecommendSys1/2_CollaborativeFiltering/userBased.py)


## 1.4 算法优化2

针对hot打压的优化。

如果两个用户同时对hot物品有过行为，这并不能说明这两个用户相似，因为大多人都对hot物品有过行为。但是，如果两个用户同时对冷门的物品有过行为，那可以说明这两个用户的兴趣是相似的。


![image](https://gitee.com/journey7878/img-bed/raw/master/RecommendSys1/picUserCF11.png)

之前的公式等同于：

![image](https://gitee.com/journey7878/img-bed/raw/master/RecommendSys1/picUserCF12.png)


区别在于ln项。其中，N(i)表示：物品i有过行为的用户集合。所以物品i越热门，N(i)就越大，w_{uv}会越小。从而减小了热门物品对用户相似度的影响。


[User-Based算法原理 (计算用户相似度优化2) - userSimilarityBest](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/RecommendSys1/2_CollaborativeFiltering/userBased.py)

这种方式算出来的相似度分整体会偏低一些。


## 1.5 实例

[基于UserCF的电影推荐系统](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/RecommendSys1/2_CollaborativeFiltering/recMovieLensUserCF.py)


## 附：公式

[latex](https://latex.codecogs.com/)

```math
W_{uv} = \frac{\left| N(u) \bigcap N(v) \right|}{\sqrt{ \left| N(u) \right| \cdot \left| N(v) \right| }}
W_{CA} = \frac{\left| (b,e) \bigcap (a,b,d) \right|}{\sqrt{\left| (b,e) \right| \cdot \left| (a,b,d) \right|} } = \frac{1}{\sqrt{2} \cdot \sqrt{3}} = \frac{1}{\sqrt{6}}
W_{CB} = \frac{\left| (b,e) \bigcap (a,c,e) \right|}{\sqrt{\left| (b,e) \right| \cdot \left| (a,c,e) \right|} } = \frac{1}{\sqrt{2} \cdot \sqrt{3}} = \frac{1}{\sqrt{6}}
W_{CD} = \frac{\left| (b,e) \bigcap (b,d,e) \right|}{\sqrt{\left| (b,e) \right| \cdot \left| (b,d,e) \right|} } = \frac{2}{\sqrt{2} \cdot \sqrt{3}} = \frac{2}{\sqrt{6}}
W_{CA} = \frac{1}{\sqrt{6}}; W_{CB} = \frac{1}{\sqrt{6}}; W_{CD} = \frac{2}{\sqrt{6}}
P(u,i) = \sum_{v \in S(u,K) \cap N(i)} {W_{uv} \cdot r_{vi}}
w_{uv} = \frac{\sum_{i \in N(u) \cap N(v)}{ \frac{1}{ln(1+\left| N(i) \right|)} }}{\sqrt{\left| N(u) \right| \cdot \left| N(v) \right|}}
W_{uv} = \frac{\left| N(u) \bigcap N(v) \right|}{\sqrt{ \left| N(u) \right| \cdot \left| N(v) \right| }} = \frac{\sum_{i \in N(u) \cap N(v)}{ 1 }}{\sqrt{\left| N(u) \right| \cdot \left| N(v) \right|}}
```



# 2. Item-CF

## 2.1 算法思路

给用户推荐：他之前喜欢物品的相似物品。所以，先找到“用户喜欢的物品”，再找到“喜欢物品的相似物品”。

![image](https://gitee.com/journey7878/img-bed/raw/master/RecommendSys1/picItemCF1.png)

举个例子：

- 用户C喜欢电影A
- 电影C和电影A相似
- 把用户C没有表达过喜好的电影C，推荐给用户C

## 2.2 算法实现

### 1 实现步骤

step1 计算物品之间的相似度

step2 计算推荐结果

### 2 举例

#### step0 构建用户物品评分表


| 姓名        | 物品a  | 物品b | 物品c | 物品d | 物品e
| ------------- |:-----|:-----|:-----|
| A | 3.0 | 4.0 | 0 | 3.5 | 0
| B | 4.0 | 0   | 4.5 | 0 | 3.5
| C | 0 | 3.5 | 0 | 0 | 3
| D | 0 | 4 |0 | 3.5 | 3


#### step1 计算物品间的相似度

还是用上面倒排表的方式做，减少稀疏矩阵的计算复杂度。

#####（1）建立用户物品倒排表

![image](https://gitee.com/journey7878/img-bed/raw/master/RecommendSys1/picItemCF2.png)

user ABCD, item abcde

#####（2）建立同现矩阵

根据用户物品倒排表，计算：同时喜欢两个物品的用户数。

就是说，如果两个物品共同被很多用户喜欢，那么这两个物品要么是因为很hot，要么就是相似。

|        | 物品a  | 物品b | 物品c | 物品d | 物品e
| ------------- |:-----|:-----|:-----|
| 物品a | 0 | 1 | 1 | 1 | 1
| 物品b | 1 | 0 | 0 | 2 | 2
| 物品c | 1 | 0 | 0 | 0 | 1
| 物品d | 1 | 2 | 0 | 0 | 1
| 物品e | 1 | 2 | 1 | 1 | 0

#####（3）计算相似度

![image](https://gitee.com/journey7878/img-bed/raw/master/RecommendSys1/picItemCF3.png)

- 分母：喜欢物品i的用户数
- 分子：同时喜欢物品i和物品j的用户数
- 公式含义：喜欢物品i的用户中，有多少比例的用户也喜欢物品j。由此衡量物品i和物品j的相似度
- 所以，物品i和物品j的相似度，与物品j和物i的相似度，是不一样的

上面同现矩阵，是分子的部分。分母如下：

|        | 有行为的用户数
| ------------- |:-----|
| 物品a | 2
| 物品b | 3
| 物品c | 1
| 物品d | 2
| 物品e | 3

所以物品之间的相似矩阵如下：

|        | 物品a  | 物品b | 物品c | 物品d | 物品e
| ------------- |:-----|:-----|:-----|
| 物品a | 0/2 | 1/2 | 1/2 | 1/2 | 1/2
| 物品b | 1/3 | 0/3 | 0/3 | 2/3 | 2/3
| 物品c | 1/1 | 0/1 | 0/1 | 0/1 | 1/1
| 物品d | 1/2 | 2/2 | 0/2 | 0/2 | 1/2
| 物品e | 1/3 | 2/3 | 1/3 | 1/3 | 0/3


#### step2 计算推荐结果

以用户C为例

|        | 评分 | 推荐结果
| ------------- |:-----|:-----|
| 物品a | 0 | [0,1/2,1/2,1/2,1/2]●[0,3.5,0,0,3]^T = 0.5 * 3.5 + 0.5 * 3 = 3.25
| 物品b | 3.5 | [1/3,0,0,2/3,2/3]●[0,3.5,0,0,3]^T = 2/3 * 3 = 2
| 物品c | 0 | [1,0,0,0,1]●[0,3.5,0,0,3]^T = 3
| 物品d | 0 | [1/2,1,0,0,1/2]●[0,3.5,0,0,3]^T = 1 * 3.5 + 1/2 * 3 = 5
| 物品e | 3 | [1/3,2/3,1/3,1/3,0]●[0,3.5,0,0,3]^T = 2/3 * 3.5 = 2.33

所以，从中去掉用户C已经评过分的物品b,e，用户对物品d的偏好最高，其次是a和c。与UserCF的结果相同。


[Item-Based算法原理](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/RecommendSys1/2_CollaborativeFiltering/itemBased.py)


## 2.3 算法优化1

针对hot打压的优化。

![image](https://gitee.com/journey7878/img-bed/raw/master/RecommendSys1/picItemCF3.png)

之前的公式是这样的。会发现一个问题，如果物品j过于热门，有很多用户进行了评分。那任何一个物品都和热门商品有很大的相似度。所以可以优化成下面的公式，降低物品j的权重，s从而减小任何物品和热门物品都会相似的可能。

![image](https://gitee.com/journey7878/img-bed/raw/master/RecommendSys1/picItemCF13.png)

两个物品有多相似，取决于他们共同被多少用户喜欢

[Item-Based算法原理 (计算用户相似度优化1) - itemSimilarityBest](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/RecommendSys1/2_CollaborativeFiltering/itemBased.py)


## 2.4 实例

[基于ItemCF的电影推荐系统](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/RecommendSys1/2_CollaborativeFiltering/recMovieLensItemCF.py)



## 附：公式

[latex](https://latex.codecogs.com/)

```math
W_{ij} = \frac{\left| N(i) \cap N(j) \right|}{\left| N(i) \right|}
W_{ij} = \frac{\left| N(i) \cap N(j) \right|}{\sqrt{ \left| N(i) \right| \left| N(j) \right|}}
```


# 3. User-CF VS Item-CF

两个算法实现的思路：

- UserCF是先找到目标用户兴趣相似的其他用户，然后将相似用户喜欢的、目标用户没有行为的item，推荐给目标用户
- ItemCF是先计算物品之间的相似度，然后根据用户历史行为和物品的相似度，为用户生成推荐列表

所以可以看出：

- UserCF算法更注重用户所在兴趣小组，容易给用户推荐所在小组中的热门商品，更注重社会化热点
- ItemCF算法更注重用户行为过的物品，所以更加个性化

## 3.1 适用场景

- UserCF利用用户间的相似度推荐。所以当物品数量远远超过用户数量的时候，考虑UserCF算法。适用场景：快消素材（新闻类、短视频类等），社交网络
- ItemCF利用物品间的相似度推荐。所以当用户数量远远超过物品数量的时候，考虑ItemCF算法。而且物品相似度相对比较稳定，可以不必要频繁更新。适用场景：非社交网站（比如要推荐一本书，理由是“和你有相似兴趣的某某也看了该书”，因为非社交，用户根本不认识某某，所以这样的推荐理由很难信服。但是，如果理由是“这本书和你之前看的某书相似”，显然更合理，用户可能就更容易接受欧系统的推荐）

## 3.2 多样性

- 单用户多样性：ItemCF不如UserCF多样性丰富。因为ItemCF推荐的是和之前行为相似的物品，物品覆盖面小，丰富度低
- 系统多样性：ItemCF多样性要远远好于UserCF。因为UserCF更注重推荐热门物品，而ItemCF更容易发现推荐长尾的物品

## 3.3 用户特点

- UserCF原则是，推荐相似用户喜欢的物品。所以，是否适应UserCF，与“他有多少相似用户”成正比
- ItemCF原则是，推荐用户历史行为物品的相似物品。所以，如果一个用户历史行为物品的自相似度大，这个用户比较符合ItemCF的基本假设，对ItemCF的适应性比价好


# 4. Item-CF VS Content-Based

这两个算法有些雷同，因为计算的都是item的相似度。但是，两者基于的item特征不同

- ContentBased算法，计算物品相似度用的是item本身的特征，比如：电影本身的特征（上映时间、导演、主演、类型、...）
- ItemCF算法，计算物品相似度用的是用户历史对item的行为，比如：基于用户对电影的评分，构建物品同现矩阵，从而计算电影间的相似度
