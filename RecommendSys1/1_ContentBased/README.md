# 1. 算法思路

基于内容的推荐算法。这个“内容”指的是，用户过去一段时间内喜欢的物品，以及由此推算出来的用户偏好。就是根据这个“内容”，为用户推荐相似物品。

就是说，向用户推荐，用户所喜欢Item的相似Item。

![image](https://gitee.com/journey7878/img-bed/raw/master/RecommendSys1/picContent1.png)

举个例子：

- 用户A和用户C喜欢爱情、浪漫类型的电影；而用户B喜欢恐怖、惊悚的电影
- 所以，将类型为“爱情、浪漫”、且用户A没有行为的电影C，推荐给用户A

# 2. 算法实现

## 2.1 实现步骤

#### Step1 构造Item特征

会用属性描述Item的特征。比如：酒店的价格、星级。

#### Step2 计算Item之间的相似度

#### Step3 评判用户是否喜欢某个Item。偏好分。


当Item数目很多时，计算每两个Item之间的相似度所产生的算法复杂度很高O(N^2)，所以进行如下优化：

- 使用训练数据得到，用户的偏好信息矩阵、物品的特征信息矩阵
- 计算用户对没有行为的Item的偏好分。实质就是，计算用户与每个Item之间的距离
- 选取偏好分topK的Item，推荐

## 2.2 举例

以movieLen电影推荐为例

#### 物品的特征信息矩阵

- ItemA 类型：Annimation, Children's, Comedy
- ItemB 类型：Adventure, Children's, Fantasy

假设，类型一共有如下几种中的一种：[Adventure, Annimation, Comedy, Children's, Fantasy]

则，向量化表示：

- ItemA = [0,1,1,1,0]
- ItemB = [1,0,0,1,1]

#### 用户的偏好信息矩阵

| 姓名        | movie1  | movie2 | movie3
| ------------- |:-----|:-----|:-----|
|张三|4|5|3
|李四 | | 1 | 4



