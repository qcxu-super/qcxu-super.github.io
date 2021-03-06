# 基础：贪心算法

贪心法：遵循某种规律，不断贪心的选取当前最优策略的算法设计方法

- 举个例子

有1元、5元、10元、20元、100元、200元的钞票无穷多张。一共需要支付X=628元，则最少需要多少张钞票？

- 规律

尽可能多的使用面额值较大的钞票。所以，628=200\*3+20\*1+5\*1+1\*3，一共需要3+1+1+3=8张

- 分析

1元、5元、10元、20元、100元、200元，任意面额是比自己小面额的倍数整数倍。所以若用较小面额钞票替换，一定需要更多的其他面额钞票。所以贪心算法的结果是全局最优解。如果增加7元面额，则贪心算法不成立。比如，X=14元。7元的问题可以用动态规划解决。

```cpp
#include <studio.h>

int main() {
    const int RMB[] = {200,100,20,10,5,1};
    const int NUM = 6; // count(ditinct RMB)
    int X = 628;
    int count = 0;
    for (int i=0; i<NUM; ++i) {
        int use = X / RMB[i];
        count += use;
        X -= RMB[i] * use;
        printf("需要面额为%d的%d张，剩余需要支付金额%d\n", RMB[i], use, X);
    }
    printf("总共需要%d张", count);
    return 0;
}
```


# 例1 [455分发饼干(easy) - 排序+贪心](https://leetcode-cn.com/problems/assign-cookies/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/3_GreedyAlgorithm/455_AssignCookies.cpp)

```
假设你是一位很棒的家长，想要给你的孩子们一些小饼干。但是，每个孩子最多只能给一块饼干。

对每个孩子 i，都有一个胃口值 g[i]，这是能让孩子们满足胃口的饼干的最小尺寸；并且每块饼干 j，都有一个尺寸 s[j] 。如果 s[j] >= g[i]，我们可以将这个饼干 j 分配给孩子 i ，这个孩子会得到满足。你的目标是尽可能满足越多数量的孩子，并输出这个最大数值。

输入: g = [1,2], s = [1,2,3]
输出: 2
解释: 
你有两个孩子和三块小饼干，2个孩子的胃口值分别是1,2。
你拥有的饼干数量和尺寸都足以让所有孩子满足。
所以你应该输出2.
```

#### 1. 规律
- 如果一块小饼干不能满足最小需求孩子，那么更大需求的孩子也不可能满足
- 如果一个孩子能被更小饼干满足，那么没必要用更大的饼干去满足。留着更大的饼干去满足需求因子更大的孩子
- 所以从需求因子小的孩子身上开始试。因为我们要的是满足的孩子尽可能多，那么把饼干8满足需求2的孩子和需求6的孩子，其实是一样的


#### 2. 解题思路
- 对饼干大小排序，对孩子需求排序。从小到大。
- 依次遍历所有饼干。只需要遍历一次。如果能满足当前孩子，那就满足了。如果不能满足当前孩子，那之后需求更大的孩子也不可能用这块饼干满足，所以这块饼干就废了
- 如果上一块饼干满足了孩子的需求，则下一块饼干，下一个孩子。如果上一块饼干没有满足孩子的需求，则上一块饼干废，到下一块饼干，还是这个孩子
- 直到没有更多的饼干，或者没有更多的孩子

```cpp
class Solution {
public:
    int findContentChildren (vector<int>& g, vector<int>& s) { //g:child. s:cookie
        std::sort(g.begin(), g.end());
        std::sort(s.begin(), s.end());
        int child = 0;
        int cookie = 0;
        while (child < g.size() && cookie < s.size()) {
            if (g[child] <= s[cookie]) {
                ++child;
            }
            ++cookie;
        }
        return child;
    }
};
```

# 例2 [376摆动序列(median) - 贪心](https://leetcode-cn.com/problems/wiggle-subsequence/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/3_GreedyAlgorithm/376_WigglSubsequence.cpp)

```
如果连续数字之间的差严格地在正数和负数之间交替，则数字序列称为摆动序列。第一个差（如果存在的话）可能是正数或负数。少于两个元素的序列也是摆动序列。

例如， [1,7,4,9,2,5] 是一个摆动序列，因为差值 (6,-3,5,-7,3) 是正负交替出现的。相反, [1,4,7,2,5] 和 [1,7,4,5,5] 不是摆动序列，第一个序列是因为它的前两个差值都是正数，第二个序列是因为它的最后一个差值为零。

给定一个整数序列，返回作为摆动序列的最长子序列的长度。 通过从原始序列中删除一些（也可以不删除）元素来获得子序列，剩下的元素保持其原始顺序。

输入: [1,17,5,10,13,15,10,5,16,8]
输出: 7
解释: 这个序列包含几个长度为 7 摆动序列，其中一个可为[1,17,10,13,10,16,8]。
```

#### 解题思路

- 连续上升的时候，应该取首尾中的一个，根据当前是连续上升/下降序列
- 举个例子，10,13,15，是连续上升序列，那么子序列中应该保留最大的，这样再下面那个才更有可能小下去，成为摇摆序列
- 反之，如果是连续下降序列，那么子序列中应该保留最小的，这样再下面的那个才更有可能高上去，成为摇摆

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic376_1.png)

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic376_2.png)

```cpp
class Solution {
public:
    int wiggleMaxLength(vector<int>& nums) {
        if (nums.size() < 2) {
            return nums.size();
        }
        static const int BEGIN = 0;
        static const int UP = 1;
        static const int DOWN = 2;
        int STATE = BEGIN;
        int max_length = 1;

        for (int i=1; i<nums.size(); ++i) {
            switch(STATE) {
            case BEGIN:
                if (nums[i-1] < nums[i]) {
                    STATE = UP;
                    ++max_length;
                }
                else if (nums[i-1] > nums[i]) {
                    STATE = DOWN;
                    ++max_length;
                }
                break;
            case UP:
                if (nums[i-1] > nums[i]) {
                    STATE = DOWN;
                    ++max_length;
                }
                break;
            case DOWN:
                if (nums[i-1] < nums[i]) {
                    STATE = UP;
                    ++max_length;
                }
                break;
            }
        }
        return max_length;
    }
};
 ```



# 例3 [402移掉K位数字(median) - 栈+贪心](https://leetcode-cn.com/problems/remove-k-digits/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/3_GreedyAlgorithm/402_RemoveKDigits.cpp)

```
给定一个以字符串表示的非负整数 num，移除这个数中的 k 位数字，使得剩下的数字最小。

输入: num = "1432219", k = 3
输出: "1219"
解释: 移除掉三个数字 4, 3, 和 2 形成一个新的最小的数字 1219。
```

#### 解题思路

- 不可能枚举，时间复杂度太高。一定是线性扫描，贪心or动态规划
- 从高位开始遍历。想要高位的数字尽可能小。所以如果高位数字大于下一位数字，就把高位数字去掉
- 上面的换种说法，后面的数字比前面的数字小的时候，把前面的去掉。那如果前面的前面数字还是大，就继续去掉前面的前面数字。所以，最最暴力的情况，要去掉K个数字，需要从最高位重新遍历K次
- 使用栈可以解决上面的问题，不用每次都从头遍历。比较栈顶和要push进来的下一个元素，如果栈顶大，则pop，继续比栈顶。直到栈为空，或者pop的数量达到K时，退出循环，把当前元素push进来，然后进行下一个元素的遍历
- 边界情况1：如果所有的都遍历完了，K还>0，比如留下1234，那么应该从后开始删K个元素
- 边界情况2：如果遇到数字0，那么如果栈空，就不push进去；如果栈不为空，就push进去

```cpp
class Solution {
public:
    string removeKdigits(string num, int k) {
        std::vector<int> s;
        std::string result = "";
        for (int i=0; i<num.length(); ++i) {
            int number = num[i] - '0';
            while (s.size() != 0 && k > 0 && s[s.size()-1] > number) {
                s.pop_back();
                --k;
            }
            if ((number==0 && s.size()>0) || number>0) {
                s.push_back(number);
            }
        }
        while (s.size() > 0 && k > 0) {
            s.pop_back();
            --k;
        }
        for (int i=0; i<s.size(); ++i) {
            result += '0' + s[i];
        }
        if (result == "") {
            result = "0";
        }
        return result;
    }
};
```

# 例4 [55跳跃游戏(median) - 贪心](https://leetcode-cn.com/problems/jump-game/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/3_GreedyAlgorithm/55_JumpGame.cpp)

```
给定一个非负整数数组 nums ，你最初位于数组的 第一个下标 。

数组中的每个元素代表你在该位置可以跳跃的最大长度。

判断你是否能够到达最后一个下标。

输入：nums = [3,2,1,0,4]
输出：false
解释：无论怎样，总会到达下标为 3 的位置。但该下标的最大跳跃长度是 0 ， 所以永远不可能到达最后一个下标。
```

#### 解题思路

- 递归的规律是，`reach_index <= i + nums[i]`
- 之所以是`<=`，是因为`nums[i]`代表了在该位置可以跳跃的最大长度，这样后面可选择的范围更大，更可能跳跃到终点 。`reach_index_max = i+nums[i]`
- 所以当`reach_index_max >= i`的时候，说明i是可达到的，`跳跃步数 = reach_index_max - i < reach_index_max`

```cpp
class Solution {
public:
    bool canJump(std::vector<int>& nums) {
        int reach = 0;
        for (int i=0; i<nums.size(); ++i) {
            if (reach < i) {
                return false;
            }
            else {
                reach = max(reach, i+nums[i]);
            }
        }
        return true;
    }
};
```


# 例5 [45跳跃游戏II(hard) - 贪心](https://leetcode-cn.com/problems/jump-game-ii/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/3_GreedyAlgorithm/45_JumpGameII.cpp)

```
给定一个非负整数数组，你最初位于数组的第一个位置。

数组中的每个元素代表你在该位置可以跳跃的最大长度。

你的目标是使用最少的跳跃次数到达数组的最后一个位置。

输入: [2,3,1,1,4]
输出: 2
```


#### 解题思路

- 同上。向`i + nums[i]`最大的那个节点跳跃，这样就可以跳到一个可以达到更远位置的位置，这样才能跳的最少
- 举个例子。例如，对于数组 [2,3,1,2,4,2,3]，初始位置是下标 0，从下标 0 出发，最远可到达下标 2。下标 0 可到达的位置中，下标 1 的值是 3，从下标 1 出发可以达到更远的位置，因此第一步到达下标 1。从下标 1 出发，最远可到达下标 4。下标 1 可到达的位置中，下标 4 的值是 4 ，从下标 4 出发可以达到更远的位置，因此第二步到达下标 4。

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic45.png)

```cpp
class Solution {
public:
    int jump(std::vector<int>& nums) {
        int step = 0;
        for (int i = 0; i < nums.size()-1; ++i) { // the last one does not need to jump
            if (i+nums[i] >= nums.size()-1) { // [2,3,1], 0+2=2
                ++step;
                break;
            }
            int max_step = nums[i];
            int expect_max_index = i;
            int expect_current_index = i;
            int best_index = i;
            for (int idx = i + 1; idx <= i + max_step && idx < nums.size(); ++idx) {
                expect_current_index = idx + nums[idx];
                if (expect_current_index >= expect_max_index) {
                    expect_max_index = expect_current_index;
                    best_index = idx;
                }
            }
            i = best_index - 1; // because next ++i
            ++step;
        }
        return step; 
    }
};
```


# 例6 [452用最少数量的箭引爆气球(median) - 排序+贪心](https://leetcode-cn.com/problems/minimum-number-of-arrows-to-burst-balloons/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/3_GreedyAlgorithm/452_MinimumNumberOfArrowsToBurstBalloons.cpp)

```
已知在一个平面上有一定数量的气球，平面可以看做一个坐标系，在平面的x轴的不同位置安排弓箭手向y轴方向射箭，弓箭可以向y轴走无穷远。

给定气球宽度 xstart <= x <= xend，问至少需要多少弓箭手，将全部气球引爆

输入：points = [[10,16],[2,8],[1,6],[7,12]]
输出：2
解释：对于该样例，x = 6 可以射爆 [2,8],[1,6] 两个气球，以及 x = 11 射爆另外两个气球
```

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic452_1.png)

#### 解题思路

- 对于某个气球，至少需要使用1只弓箭将其击穿
- 在这只气球被击穿的同时，尽可能击穿其他更多的气球。这样就可以尽可能少地使用弓箭

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic452_2.png)

所以解题步骤如下：

- 对气球按左端点从小到大进行排序
- 遍历各气球数组，同时维护一个射击区间。每遍历一个气球，满足：在可以击穿当前气球的情况下，击穿尽可能多的其他气球。每击穿一个新的气球，更新一次射击区间
- 如果新的气球无法在遍历别的气球是被带着击穿，则增加一个弓箭手。即遍历该新的气球，重新维护一个新的射击区间，重复上述遍历原则

```cpp
class Solution {
public:
    int findMinArrowShots(vector<vector<int>>& points) {
        if (points.size() == 0) {
            return 0;
        }

        std::sort(points.begin(), points.end(), cmp);

        int shoot_num = 1;
        int shoot_begin = points[0][0];
        int shoot_end = points[0][1];
        for (int i=1; i<points.size(); ++i) {
            if (points[i][0] <= shoot_end) {
                shoot_begin = points[i][0];
                if (shoot_end > points[i][1]) {
                    shoot_end = points[i][1];
                }
            }
            else {
                ++shoot_num;
                shoot_begin = points[i][0];
                shoot_end = points[i][1];
            }
        }
        return shoot_num;
    }
};
```
  
# 例7 [871最低加油次数(hard) - 堆+贪心](https://leetcode-cn.com/problems/minimum-number-of-refueling-stops/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/3_GreedyAlgorithm/871_MinimumNumberOfRefuelingStops.cpp)

```
汽车从起点出发驶向目的地，该目的地位于出发位置东面 target 英里处。

沿途有加油站，每个 station[i] 代表一个加油站，它位于出发位置东面 station[i][0] 英里处，并且有 station[i][1] 升汽油。

假设汽车油箱的容量是无限的，其中最初有 startFuel 升燃料。它每行驶 1 英里就会用掉 1 升汽油。

当汽车到达加油站时，它可能停下来加油，将所有汽油从加油站转移到汽车中。

为了到达目的地，汽车所必要的最低加油次数是多少？如果无法到达目的地，则返回 -1 。

注意：如果汽车到达加油站时剩余燃料为 0，它仍然可以在那里加油。如果汽车到达目的地时剩余燃料为 0，仍然认为它已经到达目的地。


输入：target = 100, startFuel = 10, stations = [[10,60],[20,30],[30,30],[60,40]]
输出：2
```

#### 解题思路

- 何时加油最合适？油用光的时候加油最合适！在哪个加油站加油最合适？在油量最多的加油站加油最合适！
- 怎么快速得到加油油量最大值？用最大堆！

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic871.png)

所以解题步骤如下：

- 设置一个最大堆，用来存储经过加油站的汽油量
- 按照从起点至终点的方向，遍历各个加油站之间的距离
- 每次需要走两个加油站之间的距离d，如果发现汽油不够走距离d时，从最大堆中取出一个油量添加，直到可以足够走距离d
- 如果把最大堆中的汽油全部都添加了，仍然不够前进距离d，则无法到达终点

```cpp
#include <vector>
#include <algorithm>
#include <queue>

bool cmp(const vector<int>& a, const vector<int>& b) {
    return a[0] < b[0];
}

class Solution {
public:
    int minRefuelStops(int target, int startFuel, vector<vector<int>>& stations) { // distance,fuelnum

        if (stations.size() == 0 && startFuel < target) {
            return -1;
        }

        std::sort(stations.begin(), stations.end(), cmp);

        std::priority_queue<int> big_heap;
        int result = 0;
        int total = target;

        // each station
        for (int i = 0; i < stations.size(); ++i) {
            int dist = stations[i][0]; // start--station
            int feul = stations[i][1];

            int distance = target - (total-dist); // start--station1--station2--end, target:station1--end, dist:start--station2, total:start--end
            
            startFuel -= distance;
            while (startFuel < 0) {
                if (big_heap.empty()) {
                    return -1;
                }
                startFuel += big_heap.top();
                big_heap.pop();
                ++result;
            }
            target -= distance;
            big_heap.push(feul);
        }

        // last_station--end
        if (target > 0) {
            startFuel -= target;
            while (startFuel < 0) {
                if (big_heap.empty()) {
                    return -1;
                }
                startFuel += big_heap.top();
                big_heap.pop();
                ++result;
            }
        }

        return result;
    }
};
```