# 栈基础

```cpp
#include <stdio.h>
#include <stack>

int main() {
    std::stack<int> s;
    if (s.empty()) { // s.empty()
        print("s is empty!")
    }

    s.push(5); // s.push(x)
    s.push(6);
    s.push(10);
    printf("s.top = %d\n", s.top()); // s.top()

    s.pop(); // s.pop()
    s.pop();
    printf("s.top = %d\n", s.top());
    printf("s.size = %d\n", s.size()); // s.size()
    return 0;
}
```

# 队列基础

```cpp
#include <stdio.h>
#include <queue>

int main() {
    std::queue<int> q;
    if (q.empty()) { // q.empty()
        printf("q is empty")
    }

    q.push(5); // q.push()
    q.push(6);
    q.push(10);
    printf("q.front = %d\n", q.front()) // q.front()=5

    q.pop(); // q.pop()
    q.pop();
    printf("q.front = %d\n", q.front()); // 10

    q.push(1);
    printf("q.back = %d\n", q.back()); // q.back() = 1
    printf("q.size = %d\n", q.size()); // q.size() = 2
}

```

# 堆基础

```cpp
#include <stdio.h>
#include <queue>

int main() {
    std::priority_queue<int> big_heap;
    if (big_heap.empty()) { // heap.empty()
        printf("big_heap is empty")
    }

    int test[] = {6,10,1,7,99,4,33};
    for (int i=0; i<7; ++i) {
        big_heap.push(test[i]); //heap.push()
    }
    printf("big_heap.top=%d\n",big_heap.top()); // heap.top()=99

    big_heap.push(1000); // heap.push()
    printf("big_heap.top=%d\n",big_heap.top()); // heap.top()=1000

    for (int i=0; i<3; ++i) {
        big_heap.pop() // heap.pop()
    }
    printf("big_heap.top=%d\n",big_heap.top()); // heap.top()=10
    print("big_heap.size=%d\n",big_heap.size()); // heap.size()=5
    return 0;
}
```

# 例1 [225用队列实现栈(easy)](https://leetcode-cn.com/problems/implement-stack-using-queues/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/2_StackQueueHeap/225_ImplementStackUsingQueues.cpp)

```
请你仅使用两个队列实现一个后入先出（LIFO）的栈，并支持普通队列的全部四种操作（push、top、pop 和 empty）。

["MyStack", "push", "push", "top", "pop", "empty"]
[[], [1], [2], [], [], []]
输出：
[null, null, null, 2, 2, false]
```

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic225.png)

```cpp
class MyStack {
public:
    MyStack() {

    }
    
    void push(int x) {
        std::queue<int> temp;
        temp.push(x);
        while (!_data.empty()) {
            temp.push(_data.front());
            _data.pop();
        }
        while(!temp.empty()) {
            _data.push(temp.front());
            temp.pop();
        }
    }
    
    int pop() {
        int x = _data.front();
        _data.pop();
        return x;
    }
    
    int top() {
        return _data.front();
    }
    
    bool empty() {
        return _data.empty();
    }

private:
    std::queue<int> _data;
};
```

# 例2 [232用栈实现队列(easy)](https://leetcode-cn.com/problems/implement-queue-using-stacks/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/2_StackQueueHeap/232_ImplementQueueUsingStacks.cpp)

```
请你仅使用两个栈实现先入先出队列。队列应当支持一般队列的支持的所有操作（push、pop、peek、empty）

输入：
["MyQueue", "push", "push", "peek", "pop", "empty"]
[[], [1], [2], [], [], []]
输出：
[null, null, null, 1, 1, false]
```

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic232.png)

```cpp
class MyQueue {
public:
    MyQueue() {

    }
    
    void push(int x) {
        std::stack<int> temp;
        while (!_data.empty()) {
            temp.push(_data.top());
            _data.pop();
        }
        _data.push(x);
        while (!temp.empty()) {
            _data.push(temp.top());
            temp.pop();
        }
    }
    
    int pop() {
        int x = _data.top();
        _data.pop();
        return x;
    }
    
    int peek() {
        return _data.top();
    }
    
    bool empty() {
        return _data.empty();
    }

private:
    std::stack<int> _data;
};
```

# 例3 [155最小栈(easy)](https://leetcode-cn.com/problems/min-stack/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/2_StackQueueHeap/155_MinStack.cpp)

```
设计一个支持 push ，pop ，top 操作，并能在常数时间内检索到最小元素的栈。

输入：
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]

输出：
[null,null,null,null,-3,null,0,-2]
```

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic155.png)

```cpp
class MinStack {
public:
    /** initialize your data structure here. */
    MinStack() {

    }
    
    void push(int x) {
        _data.push(x);
        if (_min.empty()) {
            _min.push(x);
        } 
        else if (_min.top() >= x) {
            _min.push(x);
        }
        else {
            _min.push(_min.top());
        }
    }
    
    void pop() {
        _data.pop();
        _min.pop();
    }
    
    int top() {
        return _data.top();
    }
    
    int getMin() {
        return _min.top();
    }
private:
    std::stack<int> _data;
    std::stack<int> _min;
};
```


# 例4 [946验证栈序列(median)](https://leetcode-cn.com/problems/validate-stack-sequences/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/2_StackQueueHeap/946_ValidateStackSequences.cpp)

```
给定 pushed 和 popped 两个序列，每个序列中的 值都不重复，只有当它们可能是在最初空栈上进行的推入 push 和弹出 pop 操作序列的结果时，返回 true；否则，返回 false 。

输入：pushed = [1,2,3,4,5], popped = [4,5,3,2,1]
输出：true
```

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic946.png)

```cpp
class Solution {模拟入栈出栈过程。跟括号匹配是同一类问题
public:
    bool validateStackSequences(vector<int>& pushed, vector<int> popped) {
        queue<int> s_popped;
        if (pushed.size() != popped.size()) {
            return false;
        }
        int n = pushed.size();
        for (int i=0; i<n; ++i) {
            s_popped.push(popped[i]);
        }

        stack<int> s;
        for (int i=0; i<n; ++i) {
            s.push(pushed[i]);
            while (!s.empty() && s.top() == s_popped.front()) {
                s.pop();
                s_popped.pop();
            }
        }
        if (s.empty()) {
            return true;
        }
        else {
            return false;
        }
    }
};
```


# 例5 [224基本计算器(hard)](https://leetcode-cn.com/problems/basic-calculator/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/2_StackQueueHeap/224_BasicCalculator.cpp)


```
实现一个基本的计算器来计算一个简单的字符串表达式 s 的值。

输入：s = "(1+(4+5+2)-3)+(6+8)"
输出：23
```

[官方题解](https://leetcode-cn.com/problems/basic-calculator/solution/ji-ben-ji-suan-qi-by-leetcode/)

思路：
- res，完整数字
- +/- 更新符号
- `(` 则把当前结果 res 和 符号入栈,
- `)` 则取出符号乘以当前结果 res，再取出res并累加


# 例6 [215数组中的第K个最大元素(median)](https://leetcode-cn.com/problems/kth-largest-element-in-an-array/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/2_StackQueueHeap/215_KthLargestElementInAnArray.cpp)

```
在未排序的数组中找到第 k 个最大的元素。请注意，你需要找的是数组排序后的第 k 个最大的元素，而不是第 k 个不同的元素。

输入: [3,2,1,5,6,4] 和 k = 2
输出: 5
```

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic215.png)

```cpp
class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        std::priority_queue<int, std::vector<int>, std::greater<int> > q;
        for (int i=0; i<nums.size(); ++i) {
            if (q.size() < k) {
                q.push(nums[i]);
            }
            else if (q.top() < nums[i]) {
                q.pop();
                q.push(nums[i]);
            }
        }
        return q.top();
    }
};
```


# 例7 [295数据流的中位数(hard)](https://leetcode-cn.com/problems/find-median-from-data-stream/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/2_StackQueueHeap/295_FindMedianFromDataStream.cpp)

```
中位数是有序列表中间的数。如果列表长度是偶数，中位数则是中间两个数的平均值。

设计一个支持以下两种操作的数据结构：

void addNum(int num) - 从数据流中添加一个整数到数据结构中。
double findMedian() - 返回目前所有元素的中位数。

输入输出:
addNum(1)
addNum(2)
findMedian() -> 1.5
addNum(3) 
findMedian() -> 2
```

![image](https://gitee.com/journey7878/img-bed/raw/master/Leetcode/pic295.png)

```cpp
class MedianFinder {
public:
    std::priority_queue<int, std::vector<int>, std::less<int> > big_heap;
    std::priority_queue<int, std::vector<int>, std::greater<int> > small_heap;
    
    MedianFinder() {
        
    }

    void addNum(int num) {
        if (big_heap.empty()) {
            big_heap.push(num);
            return;
        }
        // big_heap.size() == small_heap.size()
        if (big_heap.size() == small_heap.size() && num < small_heap.top()) {
            big_heap.push(num);
        }
        else if (big_heap.size() == small_heap.size() && num >= small_heap.top()) {
            small_heap.push(num);
        }
        // big_heap.size() < small_heap.size()
        else if (big_heap.size() < small_heap.size() && num >= small_heap.top()) {
            big_heap.push(small_heap.top());
            small_heap.pop();
            small_heap.push(num);
        }
        else if (big_heap.size() < small_heap.size() && num < small_heap.top()) {
            big_heap.push(num);
        }
        // big_heap.size() > small_heap.size(), small heap may be NULL
        else if (big_heap.size() > small_heap.size() && num > big_heap.top()) {
            small_heap.push(num);
        }
        else if (big_heap.size() > small_heap.size() && num <= big_heap.top()) {
            small_heap.push(big_heap.top());
            big_heap.pop();
            big_heap.push(num);
        }
    }

    double findMedian() {
        if (big_heap.size() == small_heap.size()) {
            return 1.0 * (big_heap.top() + small_heap.top())/2;
        }
        else if (big_heap.size() > small_heap.size()) {
            return big_heap.top();
        }
        else {
            return small_heap.top();
        }
    }
};

```