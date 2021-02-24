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