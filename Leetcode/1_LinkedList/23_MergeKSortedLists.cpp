/*
方法1 排序后相连
*/

#include <vector>
#include <algorithm>

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



/*
方法2 分治后相连
*/
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