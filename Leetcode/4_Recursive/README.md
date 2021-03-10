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


# 例5 N皇后问题

# 例6 逆序数