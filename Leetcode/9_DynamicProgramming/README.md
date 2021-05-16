利用各阶段之间的关系，逐个求解，最终求得全局最优解。

#### 关键要素：
- 原问题与子问题
- 动态规划状态
- 边界状态结值
- 状态转移方程

# 例1 [70爬楼梯(easy)](https://leetcode-cn.com/problems/climbing-stairs/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/9_DynamicProgramming/70_ClimbingStairs.cpp)

```
假设你正在爬楼梯。需要 n 阶你才能到达楼顶。
每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？

注意：给定 n 是一个正整数。
```

#### 暴力算法，递归

- timeout

```cpp
class Solution {
public:
    int climbStairs(int n) {
        if (n == 1 || n == 2) {
            return n;
        }
        return climbStairs(n-1) + climbStairs(n-2);
    }
};
```

#### 动态规划

要么1阶，要么2阶。

##### 1. 确定原问题与子问题
- 原问题：求n阶台阶所有走法的数量
- 子问题：求1阶台阶，2阶台阶，...，n-1阶台阶的走法
- 设置递推数组dp[0...n]，dp[i]表示：到达第i阶后，有多少中走法

##### 2. 确认状态
- 本题状态单一，第i个状态，即为i阶台阶的所有走法数量

##### 3. 确认边界状态的值
- 即：1阶台阶和2阶台阶的走法。
- 到达第1阶，有1种走法（只能爬1个台阶），dp[1] = 1
- 到达第2阶，有2种走法（一次性爬2阶 or 爬两次1个台阶），dp[2] = 2

##### 4. 确定状态转移方程
- 到达第i阶方式的数量 = 到达第i-1阶方式数量 + 到达第i-2阶方式数量
- dp[i] = dp[i-1] + dp[i-2]; (i>=3)

##### 5. 举例

```
dp[0] = 0
dp[1] = 1
dp[2] = 2
dp[3] = dp[1] + dp[2]
...
dp[i] = dp[i-1] + dp[i-2]
...
dp[n] = dp[n-1] + dp[n-2]
```

```cpp
# include <vector>
class Solution {
public:
    int climbStairs(int n) {
        std::vector<int> dp(n+3, 0);  // 如果n=0，前面两行就越界了，所以n+3
        dp[1] = 1;
        dp[2] = 2;
        for (int i=3; i<=n; ++i) {
            dp[i] = dp[i-1] + dp[i-2];
        }
        return dp[n];
    }
};
```


# 例2 [198打家劫舍(median)](https://leetcode-cn.com/problems/house-robber/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/9_DynamicProgramming/198_HouseRobber.cpp)

```
在一条直线上有n个房屋，每个房屋中有数量不等的财宝。有一个盗贼，希望从房屋中盗取财宝。由于房屋中有报警器，如果同时从相邻的两个房屋中刀舞财宝就会触发报警器。

问：在不触发报警器的前提下，最多可以获取多少财宝？

输入：[5,2,6,3,1,7]
输出：18 (=5+6+7)
```

#### 分析

重点在于不能相邻。0-1背包问题。

- 如果选择第i个房间盗取财宝，那一定不能选择第i-1个房间盗取财宝，所以在前i-2个房间取最优值
- 如果不选择第i个房间盗取财宝，那考虑在前i-1个房间取最优值


#### 动态规划

##### 1. 确定原问题与子问题
- 原问题：求n个房间的最优解
- 子问题：求前1个房间、前2个房间、...、前n个房间的最优解

##### 2. 确认状态
- 本题状态单一，第i个状态，即为前i个房间的最优解

##### 3. 确认边界状态的值
- 前1个房间的最优解，即第1个房间的财宝
- 前2个房间的最优解，即第1、2个房间中的较大财宝


##### 4. 确定状态转移方程
- 如果不选择第i个房间：前i-1个房间的最优解
- 如果选择第i个房间：第i个房间+前i-2个房间的最优解
- dp[i] = max(dp[i-1], dp[i-2]+nums[i]); (i>=3)

##### 5. 举例

```
[5,2,6,3,1,7]

dp[1] = 5
dp[2] = 5
dp[3] = max(dp[2], dp[1]+nums[3]) = max(5, 5+6) = 11
dp[4] = max(dp[3], dp[2]+nums[4]) = max(11, 5+3) = 11
dp[5] = max(dp[4], dp[3]+nums[5]) = max(11, 11+1) = 12
dp[6] = max(dp[5], dp[4]+nums[6]) = max(12, 11+7) = 18
```

```cpp
class Solution {
public:
    int rob(vector<int>& nums) {
        if (nums.size() == 0) {
            return 0;
        }
        if (nums.size() == 1) {
            return nums[0];
        }

        vector<int> dp(nums.size(), 0);
        dp[0] = nums[0];
        dp[1] = max(nums[0], nums[1]);
        for (int i=2; i<nums.size(); ++i) {
            dp[i] = max(dp[i-1], dp[i-2]+nums[i]);
        }
        return dp[nums.size()-1];
    }
};
```


# 例3 [53最大子序和(easy)](https://leetcode-cn.com/problems/maximum-subarray/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/9_DynamicProgramming/53_MaximumSubarray.cpp)

```
给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。

输入：nums = [-2,1,-3,4,-1,2,1,-5,4]
输出：6
解释：连续子数组 [4,-1,2,1] 的和最大，为 6 。
```

#### 分析

主要是分析dp[i]，这里i的具体含义。怎么才能让第i个状态最优解与第i-1个状态产生直接联系？重点在于连续，连续得相邻。

dp[i]表示：以第i个数字结尾的最大字段和。从举例中发现，重点在于要不要带前面那段，如果前面那段>=0，那么dp[i]=dp[i-1]+nums[i]，否则dp[i]=nums[i]。所以，dp[i]与dp[i-1]的关系是：dp[i] = max(dp[i-1]+nums[i], nums[i])


#### 动态规划

##### 1. 确定原问题与子问题
- 原问题：求长度为n的数组连续最大子序和
- 子问题：求前1个元素、前2个元素、...、前n个元素的最优解

##### 2. 确认状态
- 本题状态单一，第i个状态，即为前i个元素的最优解

##### 3. 确认边界状态的值
- 以第1个数组结尾的最大字段和 dp[0]=nums[0]

##### 4. 确定状态转移方程
- 如果dp[i-1]>=0，则：dp[i]=dp[i-1]+nums[i]
- 如果dp[i-1]<0，则：dp[i]=nums[i]
- dp[i] = max(dp[i-1]+nums[i], nums[i]); (i>=2)


##### 5. 举例

```
[-2,1,-3,4,-1,2,1,-5,4]

dp[0] = [-2]
dp[1] = -2,[1]
dp[2] = -2,[1,-3]
dp[3] = -2,1,-3,[4]
dp[4] = -2,1,-3,[4,-1]
dp[5] = -2,1,-3,[4,-1,2]
dp[6] = -2,1,-3,[4,-1,2,1]
...
```

```cpp
class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        vector<int> dp(nums.size(), 0);
        dp[0] = nums[0];
        int max_res = dp[0];
        for (int i=1; i<nums.size(); ++i) {
            dp[i] = max(dp[i-1]+nums[i], nums[i]);
            if (max_res < dp[i]) {
                max_res = dp[i];
            }
        }
        return max_res;
    }
};
```


# 例4 [322零钱兑换(median)](https://leetcode-cn.com/problems/coin-change/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/9_DynamicProgramming/322_CoinChange.cpp)

```
给定不同面额的硬币 coins 和一个总金额 amount。编写一个函数来计算可以凑成总金额所需的最少的硬币个数。如果没有任何一种硬币组合能组成总金额，返回 -1。
你可以认为每种硬币的数量是无限的。

输入：coins = [1, 2, 5], amount = 11
输出：3 
解释：11 = 5 + 5 + 1
```

#### 贪心算法

```
coins=[1,2,5,10], amount=14 --> 10+2+2  --> 3 --> right
coins=[1,2,5,7,10], amount=14  --> 10+2+2  --> 3  --> error, right is 2 (14=7+7)
```

- 贪心算法在倍数关系的数值上是可行的，但面值不确定的情况下是不可行的


#### 动态规划

背包问题。

主要是分析dp[i]，这里i的具体含义。怎么才能把金额和张数联系起来呢？

i表示金额amount，dp[i]表示满足金额的最小钞票张数。那么dp[i]就应该是 ：dp[coins[0]]+1, dp[coins[1]]+1, dp[coins[2]]+1, ... 中取最小的一个


##### 1. 确定原问题与子问题
- 原问题：求组成金额amount的最小硬币数量
- 子问题：求组成金额1,2,...,amount的最小硬币数量

##### 2. 确认状态
- 本题状态单一，第i个状态，即为前coins[k]个元素的最优解

##### 3. 确认边界状态的值
- dp[0] = 0

##### 4. 确定状态转移方程
- dp[i] = min(dp[i-coins[0]], dp[i-coins[1]], ..., dp[i-coins[k]]); (i>=2)


##### 5. 举例

```
coins=[1,2,5,7,10], amount=14

初始化：dp[i]=-1 (i>=1 and i<=14); dp[i]=1 (i=coins[k])

金额1的最优解
dp[1]=1

金额2的最优解
dp[2]=1

金额3的最优解
【方式1】3 = coins[0] + 2, dp[3] = 1 + dp[2]
【方式2】3 = coins[1] + 1, dp[3] = 1 + dp[1]
dp[3] = min(dp[2], dp[1]) + 1

金额4的最优解
【方式1】4 = coins[0] + 3, dp[4] = 1 + dp[3]
【方式2】4 = coins[1] + 2, dp[4] = 1 + dp[2]
dp[4] = min(dp[3], dp[2]) + 1

金额5的最优解
dp[5] = 1

金额6的最优解
【方式1】6 = coins[0] + 5, dp[6] = 1 + dp[5]
【方式2】6 = coins[1] + 4, dp[6] = 1 + dp[4]
【方式2】6 = coins[2] + 1, dp[6] = 1 + dp[1]
dp[6] = min(dp[5], dp[4], dp[1]) + 1

...

```

```cpp
class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        vector<int> dp;
        for (int i=0; i<=amount; ++i) {
            dp.push_back(-1);
        }

        dp[0] = 0;
        for (int i = 1; i <= amount; ++i) {
            for (int j = 0; j < coins.size(); ++j) {
                if (i == coins[j]) {
                    dp[i] = 1;
                }
                else if (i - coins[j] > 0 && dp[i-coins[j]] != -1) {
                    if (dp[i] == -1 || dp[i] > dp[i-coins[j]] + 1) {
                        dp[i] = dp[i-coins[j]] + 1;
                    }
                }
            }
        }
        return dp[amount];
    }
};
```


# 例5 [120三角形最小路径和(median)](https://leetcode-cn.com/problems/triangle/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/9_DynamicProgramming/120_Triangle.cpp)

```
给定一个三角形 triangle ，找出自顶向下的最小路径和。

每一步只能移动到下一行中相邻的结点上。相邻的结点 在这里指的是 下标 与 上一层结点下标 相同或者等于 上一层结点下标 + 1 的两个结点。也就是说，如果正位于当前行的下标 i ，那么下一步可以移动到下一行的下标 i 或 i + 1 。

输入：triangle = [[2],[3,4],[6,5,7],[4,1,8,3]]
输出：11
解释：自顶向下的最小路径和为 11（即，2 + 3 + 5 + 1 = 11）。
```

#### 分析

keyword: 相邻

从上往下，要多考虑最左和最右的边界条件。从下往上，不用考虑这个边界条件。所以，按从下往上进行推导。

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic120.png)


#### 动态规划

##### 1. 确定原问题与子问题
- 原问题：求自顶向下的最小路径和
- 子问题：求各层到各元素的最小路径和

##### 2. 确认状态
- 设置二维数组，最优值三角形dp[][]
- dp[i][j]表示：从底向上递推时，走到三角形第i行第j列的最优解

##### 3. 确认边界状态的值
- 初始化数组元素为0

##### 4. 确定状态转移方程
- 可达到(i,j)这个位置的最优解dp[i+1][j], dp[i+1][j+1]
- dp[i][j] = min(dp[i+1][j], dp[i+1][j+1]) + triangle[i][j]


```
class Solution {
public:
    int minimumTotal(vector<vector<int> >& triangle) {
        if (triangle.size() == 0) {
            return 0;
        }
        vector<vector<int> > dp;
        for (int i = 0; i < triangle.size(); ++i) {
            dp.push_back(vector<int>());
            for (int j = 0; j < triangle.size(); ++j) {
                dp[i].push_back(0);
            }
        }

        for (int j = 0; j < dp.size(); ++j) {
            dp[dp.size()-1][j] = triangle[dp.size()-1][j];
        }
        for (int i = dp.size() - 2; i >= 0; --i) {
            for (int j = 0; j < i + 1; ++j) {
                dp[i][j] = min(dp[i+1][j], dp[i+1][j+1])+triangle[i][j];
            }
        }
        return dp[0][0];
    }
};
```


# 例6 [300最长递增子序列(hard)](https://leetcode-cn.com/problems/longest-increasing-subsequence/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/9_DynamicProgramming/300_LongestIncreasingSubsequence.cpp)

```
给你一个整数数组 nums ，找到其中最长严格递增子序列的长度。

子序列是由数组派生而来的序列，删除（或不删除）数组中的元素而不改变其余元素的顺序。例如，[3,6,2,7] 是数组 [0,3,1,6,2,2,7] 的子序列。


输入：nums = [1,3,2,3,1,4]
输出：4
解释：最长递增子序列是 [1,2,3,4]，因此长度为 4 。
```

#### 暴枚举

任意元素都有选择和不选择这两种可能，所以，时间复杂度=O(n^2)。然后选择最长的子序列长度作为结果。


#### 动态规划


##### 1. 确定原问题与子问题
- 原问题：求i个元素的最长上升子序列的长度
- 子问题：求以第i个元素结尾的最长上升子序列的长度

##### 2. 确认状态
- 第i个状态，dp[i]，表示：以第i个元素结尾的最长上升子序列的长度

##### 3. 确认边界状态的值
- dp[0] = 1
- 最短就是取本身。就1个元素

##### 4. 确定状态转移方程
- dp[i] = max(dp[0]+k1, dp[1]+k2, dp[2]+k3, ..., dp[i-1]+ki)
- 如果 num[i] > num[j]，则 kj = 1，否则 kj = 0
- 最终是取最大值，这个操作跟最大字段和相似

```
dp[0] = 1, [1]
dp[1] = 2, [1,3]
dp[2] = 2, [1,2]
dp[3] = 2, [1,2,3]
dp[4] = 1, [1]

dp[5] = ?
因为dp[5]=4>num[0]，所以[1]+[4]=[1,4], 2
因为dp[5]=4>num[1]，所以[1,3]+[4]=[1,3,4], 3
因为dp[5]=4>num[2]，所以[1,2]+[4]=[1,2,4], 3
因为dp[5]=4>num[3]，所以[1,2,3]+[4]=[1,2,3,4], 4
因为dp[5]=4>num[4]，所以[1]+[4]=[1,4], 2
所以，dp[5]=max(2,3,3,4,2)=4
```

```cpp
class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        if (nums.size() == 0) {
            return 0;
        }
        vector<int> dp(nums.size(), 0);
        dp[0] = 1;
        int LIS = 1;
        for (int i = 0; i < dp.size(); ++i) {
            dp[i] = 1;
            for (int j = 0; j < i; ++j) {
                if (nums[i] > nums[j]) {
                    dp[i] = max(dp[i], dp[j] + 1);
                }
            }
            if (LIS < dp[i]) {
                LIS = dp[i];
            }
        }
        return LIS;
    }
};
```



# 例7 [64最小路径和(median)](https://leetcode-cn.com/problems/minimum-path-sum/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/9_DynamicProgramming/64_MinimumPathSum.cpp)


```
给定一个包含非负整数的 m x n 网格 grid ，请找出一条从左上角到右下角的路径，使得路径上的数字总和为最小。

说明：每次只能向下或者向右移动一步。

输入：grid = [[1,3,1],[1,5,1],[4,2,1]]
输出：7
解释：因为路径 1→3→1→1→1 的总和最小。
```

跟 [120三角形最小路径和(median)](https://leetcode-cn.com/problems/triangle/) 类似

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic64.png)

```cpp
class Solution {
public:
    int minPathSum(vector<vector<int> >& grid) {
        if (grid.size() == 0) {
            return 0;
        }
        int row = grid.size();
        int column = grid[0].size();
        vector<vector<int> > dp(row, vector<int>(column,0));
        dp[0][0] = grid[0][0];
        for (int j = 1; j < column; ++j) {
            dp[0][j] = dp[0][j-1] + grid[0][j];
        }
        for (int i = 1; i < row; ++i) {
            dp[i][0] = dp[i-1][0] + grid[i][0];
            for (int j = 1; j < column; ++j) {
                dp[i][j] = min(dp[i-1][j], dp[i][j-1]) + grid[i][j];
            }
        }
        return dp[row-1][column-1];
    }
};
```


# 例8 [174地下城游戏(hard)](https://leetcode-cn.com/problems/dungeon-game/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/9_DynamicProgramming/174_DungeonGame.cpp)


```
已知一个二维数组，左上角代表骑士的位置，右下角代表公主的位置。二维数组中存储整数，正数可以给骑士增加生命值，负数会减少骑士的生命值问骑士初始时至少是多少生命值，才可保证骑士在行走的过程中至少保持生命值为1.（骑士只能向下或向右行走）
```

要求的是，左上角的血量至少是多少。所以，肯定是从右下角往左上角推。dp[i][j]就表示，如果要达到右下角，那这个位置至少是多少血量。

##### 如果地牢是`1*1`的grid

dp[0] = max(1, 1-dungeon[0][0])。之所以要去max，是因为如果 dungeon[0][0]>0 ，则 1-dungeon[0][0] 很可能是个负数，但还是要保证到达这个点的时候，要有生命值（至少是1）。

##### 如果地牢是`1*n`或者`n*1`的grid

dp[0][i] = max(1, dp[0][i+1]-dungeon[0][i]) 或者 dp[i][0] = max(1, dp[i+1][0]-dungeon[i][0])

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic174_1.png)

##### 如果地牢是`n*m`的grid

该格结束后最少的血量值：dp_min = min(dp[i+1][j], dp[i][j+1])

到达该格最少的血量值，要活着到这个格子：dp[i][j] = max(1, dp_min-dungeon[i][j])

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic174_2.png)

```cpp
class Solution {
public:
    int calculateMinimumHP(vector<vector<int> >& dungeon) {
        if (dungeon.size() == 0) {
            return 0;
        }
        vector<vector<int> > dp(dungeon.size(), vector<int>(dungeon[0].size(), 0));
        int row = dungeon.size();
        int column = dungeon[0].size();
        dp[row-1][column-1] = max(1, 1-dungeon[row-1][column-1]);

        for (int j = column-2; j >= 0; --j) {
            dp[row-1][j] = max(1, dp[row-1][j+1]-dungeon[row-1][j]);
        }
        for (int i = row-2; i >= 0; --i) {
            dp[i][column-1] = max(1, dp[i+1][column-1]-dungeon[i][column-1]);
        }
        for (int i = row-2; i >= 0; --i) {
            for (int j = column-2; j >= 0; --j) {
                int dp_min = min(dp[i+1][j], dp[i][j+1]);
                dp[i][j] = max(1, dp_min-dungeon[i][j]);
            }
        }
        return dp[0][0];
    }
};
```
