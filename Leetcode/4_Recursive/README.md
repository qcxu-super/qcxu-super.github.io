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

#### 解题思路

- 利用回溯法生成子集，就是说，对每个元素，都有试探放入或不放入集合，这两种选择
- 选择放入该元素，递归进行后续元素的选择，完成放入该元素后续所有元素的试探
- 之后将其取出，再进行一次选择不放入该元素，递归进行后续元素的选择，完成不放入该元素后续所有元素的试探
- 选择一次放入，再选择一次不放入，这个过程就是回溯法





# 例2 生成括号

# 例3 N皇后问题

# 例4 逆序数