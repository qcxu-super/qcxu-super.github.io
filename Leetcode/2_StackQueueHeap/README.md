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

# 例1 [225用队列实现栈(easy)](https://leetcode-cn.com/problems/implement-stack-using-queues/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/2_StackQueueHeap/225_ImplementStackUsingQueues.cpp)

```
请你仅使用两个队列实现一个后入先出（LIFO）的栈，并支持普通队列的全部四种操作（push、top、pop 和 empty）。

["MyStack", "push", "push", "top", "pop", "empty"]
[[], [1], [2], [], [], []]
输出：
[null, null, null, 2, 2, false]
```

![image](https://gitee.com/XuQincheng/img-bed/raw/master/Leetcode/pic225.png)

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

![image](https://gitee.com/XuQincheng/img-bed/raw/master/Leetcode/pic232.png)

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




# 例4 合法的出栈序列

# 例5 简单的计算器

# 例6 数组中第K大的数

# 例7 寻找中位数

