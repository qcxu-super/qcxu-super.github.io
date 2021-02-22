
## 1.Leetcode

### 1.1 链表

#### 链表基础

```c++
#include <stdio.h>

struct ListNode {
    int val;
    ListNode *next;
}

int main() {
    ListNode a;
    ListNode b;
    ListNode c;
    ListNode d;
    ListNode e;
    a.val = 10;
    b.val = 20;
    c.val = 30;
    d.val = 40;
    e.val = 50;
    a.next = &b;
    b.next = &c;
    c.next = &d;
    d.next = &e;
    e.next = NULL;
    ListNode *head = &a;
    while(head) {
        printf("%d\n",head->val)
        head = head->next;
    }
    return 0;
}
```

#### 例1 [206. 反转链表 (easy)](https://leetcode-cn.com/problems/reverse-linked-list/)

[solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/src/206_ReverseLinkedList.cpp)

![image](https://gitee.com/XuQincheng/img-bed/raw/master/Leetcode/pic206.png)

#### 例2 链表逆序2 (median)

#### 例3 链表求交点 (easy)

#### 例4 链表求环 (median)

#### 例5 链表划分 (median)

#### 例6 复杂链表的复制 (hard)

#### 例7 两个排序链表归并 (easy)

#### 例8 K个排序链表归并 (hard)


