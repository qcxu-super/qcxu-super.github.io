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