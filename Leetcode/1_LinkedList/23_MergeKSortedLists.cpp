/*
方法1 排序后相连
*/

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



/*
方法2 分治后相连
*/