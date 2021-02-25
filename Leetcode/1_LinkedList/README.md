

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


# 例3 [160相交链表 (easy)](https://leetcode-cn.com/problems/intersection-of-two-linked-lists/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/1_LinkedList/160_IntersectionOfTwoLinkedLists.cpp)

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

# 例4 [142环形链表 II(median)](https://leetcode-cn.com/problems/linked-list-cycle-ii/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/1_LinkedList/142_LinkedListCycleII.cpp)

```
给定一个链表，返回链表开始入环的第一个节点。 如果链表无环，则返回 null。

为了表示给定链表中的环，我们使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。 如果 pos 是 -1，则在该链表中没有环。注意，pos 仅仅是用于标识环的情况，并不会作为参数传递到函数中。

如果链表中存在环，则返回 true 。 否则，返回 false 。

输入：head = [3,2,0,-4], pos = 1
输出：true
解释：链表中有一个环，其尾部连接到第二个节点。
```

![image](https://gitee.com/XuQincheng/img-bed/raw/master/Leetcode/pic160.png)

```cpp
class Solution {
public:
    ListNode *detectCycle(ListNode *head) {
        ListNode *fast = head;
        ListNode *slow = head;
        ListNode *meet = NULL;
        while (fast) {
            slow = slow->next;
            fast = fast->next;
            if (fast == NULL) {
                return NULL;
            }
            fast = fast->next;

            if (slow == fast) {
                meet = fast;
                break;
            }
        }

        if (meet == NULL) {
            return NULL;
        }
        while (head && meet) {
            if (head == meet) {
                return head;
            }
            head = head->next;
            meet = meet->next;
        }
        return NULL;
    }
};
```


# 例5 [86分隔链表(median)](https://leetcode-cn.com/problems/partition-list/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/1_LinkedList/86_PartitionList.cpp)

```
给你一个链表的头节点 head 和一个特定值 x ，请你对链表进行分隔，使得所有 小于 x 的节点都出现在 大于或等于 x 的节点之前。
你应当 保留 两个分区中每个节点的初始相对位置。

输入：head = [1,4,3,2,5,2], x = 3
输出：[1,2,2,4,3,5]
```

![image](https://gitee.com/XuQincheng/img-bed/raw/master/Leetcode/pic86.png)

```cpp
class Solution {
public:
    ListNode* partition(ListNode* head, int x) {
        ListNode less_head(0);
        ListNode more_head(0);
        ListNode *less_ptr = &less_head;
        ListNode *more_ptr = &more_head;
        while (head) {
            if (head->val < x) {
                less_ptr->next = head;
                less_ptr = less_ptr->next;
            }
            else {
                more_ptr->next = head;
                more_ptr = more_ptr->next;
            }
            head = head->next;
        }
        less_ptr->next = more_head.next;
        more_ptr->next = NULL;
        return less_head.next;
    }
};
```


# 例6 [138复制带随机指针的链表(median)](https://leetcode-cn.com/problems/copy-list-with-random-pointer/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/1_LinkedList/138_CopyListWithRandomPointer.cpp)

```
已知一个复杂的链表，节点中有一个指向本链表任意某个节点的随机指针（也可以为空），求这个链表的深度拷贝

输入：head = [[7,null],[13,0],[11,4],[10,2],[1,0]]
输出：[[7,null],[13,0],[11,4],[10,2],[1,0]]
```

![image](https://gitee.com/XuQincheng/img-bed/raw/master/Leetcode/pic138.png)

```cpp
class Solution {
public:
    Node* copyRandomList(Node* head) {
        std::map<Node*, int> node_map; //{add_old1:No1,add_old2:No2,add_old3:No3...}
        std::vector<Node*> node_vec; //[add_new1,add_new2,add_new3,...]
        Node *ptr = head;

        int i = 0;
        while (ptr) {
            node_map[ptr] = i;
            node_vec.push_back(new Node(ptr->val));
            ptr = ptr->next;
            i++;
        }
        node_vec.push_back(0);

        ptr = head;
        i = 0;
        while (ptr) {
            node_vec[i]->next = node_vec[i+1];
            if (ptr->random) {
                int id = node_map[ptr->random];
                node_vec[i]->random = node_vec[id];
            }
            ptr = ptr->next;
            i++;
        }

        return node_vec[0];
    }
};
```

# 例7 [21合并两个有序链表(easy)](https://leetcode-cn.com/problems/merge-two-sorted-lists/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/1_LinkedList/21_MergeTwoSortedLists.cpp)

```
将两个升序链表合并为一个新的 升序 链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。

输入：l1 = [1,2,4], l2 = [1,3,4]
输出：[1,1,2,3,4,4]
```

![image](https://gitee.com/XuQincheng/img-bed/raw/master/Leetcode/pic21.png)

```cpp
class Solution {
public:
    ListNode* mergeTwoLists(ListNode* l1, ListNode* l2) {
        ListNode l3(0);
        ListNode *ptr = &l3;
        while (l1 && l2) {
            if (l1->val < l2->val) {
                ptr->next = l1;
                l1 = l1->next;
            }
            else {
                ptr->next = l2;
                l2 = l2->next;
            }
            ptr = ptr->next;
        }
        if (l1) {
            ptr->next = l1;
        }
        if (l2) {
            ptr->next = l2;
        }
        return l3.next;
    }
};
```

# 例8 [23合并K个升序链表(hard)](https://leetcode-cn.com/problems/merge-k-sorted-lists/) | [solution](https://github.com/qcxu-super/qcxu-super.github.io/blob/master/Leetcode/1_LinkedList/23_MergeKSortedLists.cpp)

```
给你一个链表数组，每个链表都已经按升序排列。
请你将所有链表合并到一个升序链表中，返回合并后的链表。

输入：lists = [[1,4,5],[1,3,4],[2,6]]
输出：[1,1,2,3,4,4,5,6]
```

- 方法1 排序后相连

```cpp
# include <vector>
# include <algorithm>

bool cmp(const ListNode *a, const ListNode *b) {
    return a->val < b->val;
}

class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        vector<ListNode*> node_vec;
        for (int i=0; i<lists.size(); ++i) {
            ListNode *head = lists[i];
            while (head) {
                node_vec.push_back(head);
                head = head->next;
            }
        }
        if (node_vec.size()==0) {
            return NULL;
        }

        sort(node_vec.begin(), node_vec.end(), cmp);

        for (int i=0; i<node_vec.size()-1; ++i) {
            node_vec[i]->next = node_vec[i+1];
        }
        node_vec[node_vec.size()-1]->next = NULL;
        return node_vec[0];
    }
};
```

- 方法2 分治后相连

```cpp
class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        if (lists.size() == 0) {
            return NULL;
        }
        if (lists.size() == 1) {
            return lists[0];
        }
        if (lists.size() == 2) {
            return mergeTwoLists(lists[0],lists[1]);
        }

        vector<ListNode*> sub1_list;
        vector<ListNode*> sub2_list;
        int mid = lists.size() / 2;
        for (int i=0; i<mid; ++i) {
            sub1_list.push_back(lists[i]);
        }
        for (int i=mid; i<lists.size();++i) {
            sub2_list.push_back(lists[i]);
        }

        ListNode *l1 = mergeKLists(sub1_list);
        ListNode *l2 = mergeKLists(sub2_list);

        return mergeTwoLists(l1,l2);
    }
}
;
```