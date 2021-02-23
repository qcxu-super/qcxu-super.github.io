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