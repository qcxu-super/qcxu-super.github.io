

# 链表基础

```cpp
#include <stdio.h>

struct ListNode {
    int val;
    ListNode *next;
}

int main() {
    ListNode a;
    ListNode b;
    ListNode c;
    a.val = 10;
    b.val = 20;
    c.val = 30;
    a.next = &b;
    b.next = &c;
    c.next = NULL;
    ListNode *head = &a;
    while(head) {
        printf("%d\n",head->val)
        head = head->next;
    }
    return 0;
}
```

# 例1 [206反转链表 (easy)](https://leetcode-cn.com/problems/reverse-linked-list/) |  [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/1_LinkedList/206_ReverseLinkedList.cpp)

```
输入: 1->2->3->4->5->NULL
输出: 5->4->3->2->1->NULL
```

![image](https://gitee.com/XuQincheng/img-bed/raw/master/Leetcode/pic206.png)

```cpp
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode *new_head = NULL;
        while(head) {
            ListNode *next = head->next;
            head->next = new_head;
            new_head = head;
            head = next;
        }
        return new_head;
    }
}
```

# 例2 [92链表逆序2 (median)](https://leetcode-cn.com/problems/reverse-linked-list-ii/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/1_LinkedList/92_ReverseLinkedListII.cpp)

```
反转从位置 m 到 n 的链表。请使用一趟扫描完成反转。 1 ≤ m ≤ n ≤ 链表长度。

输入: 1->2->3->4->5->NULL, m = 2, n = 4
输出: 1->4->3->2->5->NULL
```

![image](https://gitee.com/XuQincheng/img-bed/raw/master/Leetcode/pic92_1.png)

![image](https://gitee.com/XuQincheng/img-bed/raw/master/Leetcode/pic92_2.png)

```cpp
class Solution {
public:
    ListNode* reverseBetween(ListNode* head, int left, int right) {
        ListNode *result = head;
        int change_len = right - left + 1;
        // pre_head
        ListNode *pre_head = NULL;
        while (head && left>1) {
            pre_head = head;
            head = head->next;
            left--;
        }
        // right -> left
        ListNode *modify_list_tail = head; // left
        ListNode *new_head = NULL; // right
        while (head && change_len>0) {
            ListNode *next = head->next;
            head->next = new_head;
            new_head = head;
            head = next;
            change_len--;
        }
        // left -> tail
        modify_list_tail->next = head;
        //pre_head -> right
        if (pre_head) {
            pre_head->next = new_head;
        }
        else {
            result = new_head;
        }
        return result;
    }
};
```


# 例3 [160相交链表 (median)](https://leetcode-cn.com/problems/intersection-of-two-linked-lists/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/1_LinkedList/160_IntersectionOfTwoLinkedLists.cpp)

```
找到两个单链表相交的起始节点

输入：intersectVal = 8, listA = [4,1,8,4,5], listB = [5,0,1,8,4,5], skipA = 2, skipB = 3
输出：Reference of the node with value = 8
输入解释：相交节点的值为 8 （注意，如果两个链表相交则不能为 0）。从各自的表头开始算起，链表 A 为 [4,1,8,4,5]，链表 B 为 [5,0,1,8,4,5]。在 A 中，相交节点前有 2 个节点；在 B 中，相交节点前有 3 个节点。
```

![image](https://gitee.com/XuQincheng/img-bed/raw/master/Leetcode/pic160.png)

```cpp
class Solution {
public:
    ListNode *getIntersectionNode(ListNode *headA, ListNode *headB) {
        int len_a = get_list_length(headA);
        int len_b = get_list_length(headB);
        if (len_a > len_b) {
            headA = forward_long_list(len_a, len_b, headA);
        }
        else {
            headB = forward_long_list(len_b, len_a, headB);
        }
        
        while (headA && headB) {
            if (headA == headB) {
                return headA;
            }
            headA = headA->next;
            headB = headB->next;
        }
        return NULL;
    }
};
```


# 例4 链表求环 (median)

# 例5 链表划分 (median)

# 例6 复杂链表的复制 (hard)

# 例7 两个排序链表归并 (easy)

# 例8 K个排序链表归并 (hard)


