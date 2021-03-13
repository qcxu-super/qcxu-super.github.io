# 基础：递归

只是开发代码的一种方式

#### 计算1+2+3

```cpp
#include <studio.h>
void compute_sum_3(int i, int &sum) {
    sum += i;
}
void compute_sum_2(int i, int &sum) {
    sum += i;
    compute_sum_3(i+1, sum);
}
void compute_sum_1(int i, int &sum) {
    sum += i;
    compute_sum_2(i+1, sum);
}
int main() {
    int sum = 0;
    compute_sum_1(1,sum);
    printf('sum = %d\n', sum);
    return 0;
}
```

可以写成一个函数，自己调用自己去实现。

```cpp
#include <studio.h>
void compute_sum(int i, int &sum) {
    if (i > 3){ // end
        return;
    }
    sum += i;
    compute_sum(i+1, sum);
}
int main() {
    int sum = 0;
    compute_sum(1, sum);
    printf('sum = %d\n', sum);
    return 0;
}
```

#### 链表

```cpp
#include <studio.h>
#include <vector>

struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x): val(x), next(NULL) {}
};
void add_to_vector(ListNode* head, vector<int>& vec) {
    if (!head) { // head==NULL
        return;
    }
    vec.push_back(head->val);
    add_to_vector(head->next, vec);
}
int main() {
    ListNode a(1);
    ListNode b(2);
    ListNode c(3);
    a.next = &b;
    b.next = &c;
    vector<int> vec;
    add_to_vector(&a, vec);
    for (int i=0; i<vec.size(); ++i) {
        printf('[%d]', vec[i]);
    }
    return 0;
}

```

# 基础：回溯 

回溯算法，也称试探法。当探索到某一步时，发现原先选择达不到目标，就退回一步重新选择。这种走不通就退回再走的技术成为回溯法。

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic004.png)

#### 求子集

```cpp
#include <studio.h>
#include <vector>

int main() {
    vector<int> nums;
    nums.push_back(1);
    nums.push_back(2);
    nums.push_back(3);

    vector<int> item;
    vector<vector<int>> result;

    for (int i=0; i<nums.size(); ++i) {
        item.push_back(nums[i]); // i=0:item=[1], i=2:item=[1,2], i=3:item=[1,2,3]
        result.push_back(item); // [[1],[1,2],[1,2,3]]
    }

    for (int i=0; i<result.size(); ++i) {
        for (int j=0; j<result[i].size(); ++j) {
            print('[%d]', result[i][j]); // [1]\n[1][2]\n[1][2][3]\n
        }
        printf('\n')
    }
    return 0;
}
```

上面使用循环实现的。但可以用递归的方式实现！

```cpp
#include <studio.h>
#include <vector>

void generator(int i, vector<int>& nums, vector<int>& item, vector<vector<int>>& result) {
    if (i >= nums.sie()) {
        return;
    }
    item.push_back(nums[i]);
    result.push_back(item);
    generator(i+1, nums, item, result);
}

int main() {
    vector<int> nums;
    nums.push_back(1);
    nums.push_back(2);
    nums.push_back(3); // nums=[1,2,3]
    vecor<int> item;
    vector<vector<int>> result;
    generator(0, nums, item, result); // recursive
    for (int i=0; i<result.size(); ++i) {
        for (int j=0; j<result[i].size(); ++j) {
            print('[%d]', result[i][j]); // [1]\n[1][2]\n[1][2][3]\n
        }
        printf('\n')
    }
    return 0;
}
```

# 基础：分治法、归并排序

已知两个已排序数组，将这两个数组合并为一个排序数组

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic044_1.png)

```cpp
void merge_sort_two_vec(vector<int>& sub_vec1, vector<int>& sub_vec2, vector<int>& vec) {
    int i = 0;
    int j = 0;
    while (i < sub_vec1.size() && j < sub_vec2.size()) {
        if (sub_vec1[i] <= sub_vec2[j]) {
            vec.push_back(sub_vec1[i]);
            ++i;
        }
        else {
            vec.push_back(sub_vec2[j]);
            ++j;
        }
    }
    for (; i < sub_vec1.size(); ++i) {
        vec.push_back(sub_vec1[i]);
    }
    for (; j < sub_vec2.size(); ++j) {
        vec.push_back(sub_vec2[j]);
    }
}
```

上面这个有什么用？归并排序会用到！利用分治算法做归并排序！

- 什么是分治算法？将一个规模为N的问题，分解为K个规模较小的子问题，这些问题相互独立，且与原问题的性质相同。求出子问题的解后进行合并，就可以得到原问题的解。
- 利用分治算法，可以对一个无序的数组进行归并排序
- Step1 分解，把一个无序的数组分解成若干个无序的数组
- Step2 求解，对若干的无序数组进行排序，这样得到若干个已经排好序的子数组
- Step3 合并，利用上面的思路，将子数组逐个合并，得到完整的排序
- 时间复杂度：`分解时间 + 解决子问题时间 + 合并时间 = O(n) + 2T(n/2) + O(n) = O(n + 2*n/2 + 4*n/4 + ...) = O(nlogn)`

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic044_2.png)

```cpp
void merge_sort(vector<int>& vec) {
    if (vec.size() < 2) {
        return; // solution
    }

    // Step1
    int mid = vec.size() / 2;
    vector<int> sub_vec1;
    vector<int> sub_vec2;
    for (int i=0; i<mid; ++i) {
        sub_vec1.push_back(vec[i]);
    }
    for (int i=mid; i<vec.size(); ++i) {
        sub_vec2.push_back(vec[i]);
    }

    // Step2
    merge_sort(sub_vec1);
    merge_sort(sub_vec2);
    vec.clear();

    // Step3
    merge_sort_two_vec(sub_vec1,sub_vec2,vec);
}
```



# 例1 [78子集(median)](https://leetcode-cn.com/problems/subsets/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/4_Recursive/78_Subsets.cpp)

```
给你一个整数数组 nums ，数组中的元素 互不相同 。返回该数组所有可能的子集（幂集）。

解集 不能 包含重复的子集。你可以按 任意顺序 返回解集。

输入：nums = [1,2,3]
输出：[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
```

#### 解题思路1 回溯法

- 利用回溯法生成子集，就是说，对每个元素，都有试探放入或不放入集合，这两种选择
- 选择放入该元素，递归进行后续元素的选择，完成放入该元素后续所有元素的试探
- 之后将其取出，再进行一次选择不放入该元素，递归进行后续元素的选择，完成不放入该元素后续所有元素的试探
- 选择一次放入，再选择一次不放入，这个过程就是回溯法


![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic78.png)

- 红色部分是第一次递归调用（放），蓝色部分是pop出来第二次递归调用（不放）
- 是暴力解算的方法之一

```cpp
class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> result;
        vector<int> item;
        result.push_back(item);
        generate(0,nums,item,result);
        return result;
    }
private:
    void generate(int i, vector<int>& nums, vector<int>& item, vector<vector<int>>& result) {
        if (i >= nums.size()) {
            return;
        }
        item.push_back(nums[i]); // put nums[i]
        result.push_back(item);
        generate(i+1, nums, item, result);
        item.pop_back(); // not put nums[i]
        generate(i+1, nums, item, result);
    }
};
```

#### 解题思路2 位运算法

- A:100, B:010, C:001

subset | value | A | B | C
---|---|---|---|---
{} | 000=0 | 0=100&000 | 0=010&000 | 0=001&000
{C} | 001=1 | 0=100&001 | 0=010&001 | 1=001&001
{B} | 010=2 | 0=100&010 | 1=010&010 | 0=001&010
{B,C} | 011=3 | 0=100&011 | 1=010&011 | 1=001&011
{A} | 100=4 | 1=100&100 | 0=010&100 | 0=001&100
{A,C} | 101=5 | 1=100&101 | 0=010&101 | 1=001&101
{A,B} | 110=6 | 1=100&110 | 1=010&110 | 0=001&110
{A,B,C} | 111=7 | 1=100&111 | 1=010&111 | 1=001&111

```cpp
class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> result;
        int all_set = 1<<nums.size(); // 2^n. 0001<<3=1000=8=2^3
        for (int i=0; i<all_set; ++i) {
            vector<int> item;
            for (int j=0; j<nums.size(); ++j) {
                if (i & (1<<j)) { //0:001,1:010,2:100
                    item.push_back(nums[j]);
                }
            }
            result.push_back(item);
        }
        return result;
    }
};
```

# 例2 [90子集II(median)](https://leetcode-cn.com/problems/subsets-ii/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/4_Recursive/90_SubsetsII.cpp)

```
给定一个可能包含重复元素的整数数组 nums，返回该数组所有可能的子集（幂集）。

说明：解集不能包含重复的子集。

输入: [1,2,2]
输出:
[
  [2],
  [1],
  [1,2,2],
  [2,2],
  [1,2],
  []
]
```

#### 解题思路

- vector不能重复。用set对vector进行去重

```
class Solution {
public:
    vector<vector<int>> subsetsWithDup(vector<int>& nums) {
        vector<vector<int>> result;
        vector<int> item;
        set<vector<int>> res_set;
        sort(nums.begin(), nums.end());
        result.push_back(item);
        generate(0,nums,result,item,res_set);
        return result;
    }
private:
    void generate(int i, vector<int>& nums, vector<vector<int>>& result, vector<int>& item, set<vector<int>>& res_set) {
        if (i >= nums.size()) {
            return;
        }
        item.push_back(nums[i]);
        if (res_set.find(item) == res_set.end()) { // not find in set
            result.push_back(item);
            res_set.insert(item);
        }
        generate(i+1, nums, result, item, res_set); // put nums[i]
        item.pop_back();
        generate(i+1, nums, result, item, res_set); // not put nums[i]
    }
};
```

# 例3 [40组合总和II(median)](https://leetcode-cn.com/problems/combination-sum-ii/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/4_Recursive/40_CombinationSumII.cpp)

```
给定一个数组 candidates 和一个目标数 target ，找出 candidates 中所有可以使数字和为 target 的组合。

candidates 中的每个数字在每个组合中只能使用一次。

输入: candidates = [10,1,2,7,6,1,5], target = 8,
所求解集为:
[
  [1, 7],
  [1, 2, 5],
  [2, 6],
  [1, 1, 6]
]
```

#### 解题思路

- 当选择某几个元素，之和>target时，就不用再往下递归了。这个过程叫剪枝。可以大幅度提升效率
- 剪枝在深度搜索里面非常常用

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic40.png)

```cpp
class Solution {
public:
    vector<vector<int>> combinationSum2(vector<int>& candidates, int target) {
        vector<vector<int>> result;
        vector<int> item;
        set<vector<int>> res_set;
        sort(candidates.begin(),candidates.end());
        generate(0,candidates,result,item,res_set,0,target);
        return result;
    }

    void generate(int i, vector<int>& nums, vector<vector<int>>& result, vector<int>& item, set<vector<int>>& res_set, int sum, int target) {
        if (i >= nums.size() || sum > target) {
            return;
        }
        sum += nums[i];
        item.push_back(nums[i]);
        if (sum == target && res_set.find(item) == res_set.end()) {
            result.push_back(item);
            res_set.insert(item);
        }
        generate(i+1, nums, result, item, res_set, sum, target);
        sum -= nums[i];
        item.pop_back();
        generate(i+1, nums, result, item, res_set, sum, target);
    }

};
```


# 例4 [22括号生成(median)](https://leetcode-cn.com/problems/generate-parentheses/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/4_Recursive/22_GenerateParentheses.cpp)

```
数字 n 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且 有效的 括号组合。

输入：n = 3
输出：["((()))","(()())","(())()","()(())","()()()"]
```

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic22.png)

```cpp
class Solution {
public:
    vector<string> generateParenthesis(int n) {
        vector<string> result;
        generate("",n,n,result);
        return result;
    }

private:
    void generate(string item, int left, int right, vector<string>& result) {
        if (left == 0 && right == 0) {
            result.push_back(item);
            return;
        }
        if (left > 0) {
            generate(item+'(', left-1, right, result);
        }
        if (left < right) { // '(' is more then ')' in item
            generate(item+')', left, right-1, result);
        }
    }
};
```

# 例5 [51N皇后(hard)](https://leetcode-cn.com/problems/n-queens/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/4_Recursive/51_NQueens.cpp)

```
n 皇后问题 研究的是如何将 n 个皇后放置在 n×n 的棋盘上，并且使皇后彼此之间不能相互攻击。

给你一个整数 n ，返回所有不同的 n 皇后问题 的解决方案。

每一种解法包含一个不同的 n 皇后问题 的棋子放置方案，该方案中 'Q' 和 '.' 分别代表了皇后和空位。
```

![image](https://assets.leetcode.com/uploads/2020/11/13/queens.jpg)

```
输入：n = 4
输出：[[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
解释：如上图所示，4 皇后问题存在两个不同的解法。
```

#### 解题思路

- 什么叫不能互相攻击？横竖斜不能放两个皇后！
- 怎么表示不能相互攻击？核心在于怎么表示棋盘和皇后！定义方向数组！依次表示：左、右、上、下、左上、左下、右上、右下

```cpp
static const int dx[] = {-1,1,0,0,-1,-1,1,1};
static const int dy[] = {0,0,-1,1,-1,1,-1,1};
```

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic51.png)

- `n`个皇后，放在`n×n`的棋盘上，所以每行有且只有1个皇后。所以应该是，依次遍历每一行，回溯算法决定放置在哪一列，保证是不会被攻击到的列

```cpp
class Solution {
public:
    vector<vector<string>> solveNQueens(int n) {
        vector<vector<string>> result; // [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
        vector<string> location; // [".Q..","...Q","Q...","..Q."]
        vector<vector<int>> mark; // [[1,1,1,1],[1,1,0,0],[1,0,1,0],[1,0,0,1]]]
        // init mark
        for (int i=0; i<n; ++i) {
            vector<int> m;
            for (int j=0; j<n; ++j) {
                m.push_back(0);
            }
            mark.push_back(m);
        }
        // init location
        for (int i=0; i<n; ++i) {
            string s = "";
            for (int j=0; j<n; ++j) {
                s.append(".");
            }
            location.push_back(s);
        }
        // put queen
        generate(0,n,location,result,mark);
        return result;
    }
private:
    void put_down_the_queen(int x, int y, vector<vector<int>>& mark) {
        static const int dx[] = {-1,1,0,0,-1,-1,1,1};
        static const int dy[] = {0,0,-1,1,-1,1,-1,1};
        mark[x][y] = 1;
        for (int i=0; i<mark.size(); ++i) { // max delta is mark.size()
            for (int j=0; j<8; ++j) { // iteration on direction
                int new_x = x + i * dx[j];
                int new_y = y + i * dy[j];
                if (new_x >= 0 && new_x < mark.size() && new_y >= 0 && new_y < mark.size()) {
                    mark[new_x][new_y] = 1;
                }
            }
        }
    }

    void generate(int i, int n, vector<string>& location, vector<vector<string>>& result, vector<vector<int>>& mark) {
        if (i == n) {
            result.push_back(location);
            return;
        }
        for (int j=0; j<n; ++j) {
            if (mark[i][j] == 0) {
                vector<vector<int>> tmp_mark = mark;
                location[i][j] = 'Q';
                put_down_the_queen(i,j,mark);
                generate(i+1, n, location, result, mark);
                mark = tmp_mark;
                location[i][j] = '.';
            }
        }
    }
};
```

# 例6 [315计算右侧小于当前元素的个数(hard)](https://leetcode-cn.com/problems/count-of-smaller-numbers-after-self/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/4_Recursive/315_CountOfSmallerNumbersAfterSelf.cpp)

```
给定一个整数数组 nums，按要求返回一个新数组 counts。数组 counts 有该性质： counts[i] 的值是  nums[i] 右侧小于 nums[i] 的元素的数量。

输入：nums = [5,2,6,1]
输出：[2,1,1,0] 
解释：
5 的右侧有 2 个更小的元素 (2 和 1)
2 的右侧仅有 1 个更小的元素 (1)
6 的右侧有 1 个更小的元素 (1)
1 的右侧有 0 个更小的元素
```


#### 解题思路

- 最最暴力的方法，对每个元素扫描其右边比它小的数，累加个数。假设数组元素个数是n，则时间复杂度是：O(n)
- 但如果用归并排序的思路，边归并排序边统计解题，时间复杂度是：O(nlogn)
- 既要知道该值的大小（作排序用），又要知道该值index位置（从小到大排序，有多少元素排到当前元素前面，把该值累加到当前元素的index上）。所以要形成pair对后，再进行归并排序
- 归并时计算，当前值右侧有多少是小于当前值的？举个例子，重点看下图最后一层。有两个从小到大排序的vector，[-7,1,5,9],[-2,1,3,5]，计算每个元素右边有多少是小于当前值的。首先，同一个vector里面这个统计值一定是0，因为各vector之间是按照从小到大排序的，右边的数不可能比左边的再小。所以第二个vector所有元素这个统计值一定是0。而第一个vector只要统计第二个vector里面有多少是小于当前元素的，也就是遍历第二个vector的j。具体地，-7后面没有比它小的，所以1位置+0；1后面有1个更小的-2，所以3位置+1；5后面有3个更小的-2,1,3，所以0位置+3；9后面都比他小，所以2位置+4；第二个vector所有index位置全部都是+0。

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic315.png)


```cpp
class Solution {
public:
    vector<int> countSmaller(vector<int>& nums) {
        vector<pair<int,int>> vec;
        vector<int> count;
        for (int i=0; i<nums.size(); ++i) {
            vec.push_back(make_pair(nums[i],i));
            count.push_back(0);
        }
        merge_sort(vec, count);
        return count;
    }

private:
    void merge_sort_two_vec(vector<pair<int,int>>& sub_vec1, vector<pair<int,int>>& sub_vec2, vector<pair<int,int>>& vec, vector<int>& count) {
        int i = 0;
        int j = 0;
        while (i < sub_vec1.size() && j < sub_vec2.size()) {
            if (sub_vec1[i].first <= sub_vec2[j].first) {
                vec.push_back(sub_vec1[i]);
                count[sub_vec1[i].second] += j; //
                ++i;
            }
            else {
                vec.push_back(sub_vec2[j]);
                ++j;
            }
        }
        for (; i < sub_vec1.size(); ++i) {
            count[sub_vec1[i].second] += j; //
            vec.push_back(sub_vec1[i]);
        }
        for (; j < sub_vec2.size(); ++j) {
            vec.push_back(sub_vec2[j]);
        }
    }

    void merge_sort(vector<pair<int,int>>& vec, vector<int>& count) {
        if (vec.size() < 2) {
            return; // solution
        }

        // Step1
        int mid = vec.size() / 2;
        vector<pair<int,int>> sub_vec1;
        vector<pair<int,int>> sub_vec2;
        for (int i=0; i<mid; ++i) {
            sub_vec1.push_back(vec[i]);
        }
        for (int i=mid; i<vec.size(); ++i) {
            sub_vec2.push_back(vec[i]);
        }

        // Step2
        merge_sort(sub_vec1, count);
        merge_sort(sub_vec2, count);
        vec.clear();

        // Step3
        merge_sort_two_vec(sub_vec1,sub_vec2,vec,count);
    }
};
```