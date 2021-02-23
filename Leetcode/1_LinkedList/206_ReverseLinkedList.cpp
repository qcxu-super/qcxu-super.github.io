struct ListNode {
    int val;
    ListNode *next;
    ListNode(int x): val(x), next(nullptr) {}
}

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