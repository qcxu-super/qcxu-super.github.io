int get_list_length(ListNode *head) {
    int len = 0;
    while (head) {
        len++;
        head = head->next;
    }
    return len;
}

ListNode *forward_long_list(int long_len, int short_len, ListNode *head) {
    int delta = long_len - short_len;
    while (head && delta > 0) {
        head = head->next;
        delta--;
    }
    return head;
}


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