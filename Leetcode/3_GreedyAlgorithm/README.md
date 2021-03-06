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

- 递归的规律是，reach_index<=i+nums[i]
- 之所以是<=，是因为nums[i]代表了在该位置可以跳跃的最大长度，这样后面可选择的范围更大，更可能跳跃到终点 。reach_index_max=i+nums[i]
- 所以当reach_index_max>=i的时候，说明i是可达到的，跳跃步数=reach_index_max-i<reach_index_max

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

```cpp
给定一个非负整数数组，你最初位于数组的第一个位置。

数组中的每个元素代表你在该位置可以跳跃的最大长度。

你的目标是使用最少的跳跃次数到达数组的最后一个位置。

输入: [2,3,1,1,4]
输出: 2
```


# 例6 射击气球（排序+贪心）
  
# 例7 最优加油方法（堆+贪心）