class Node {
public:
    int val;
    Node* next;
    Node* random;
    
    Node(int _val) {
        val = _val;
        next = NULL;
        random = NULL;
    }
};


class Solution {
public:
    Node* copyRandomList(Node* head) {
        std::map<Node*, int> node_map; //{add_old1:No1,add_old2:No2,add_old3:No3...}
        std::vector<Node*> node_vec; //[add_new1,add_new2,add_new3,...]
        Node *ptr = head;

        int i = 0;
        while (ptr) {
            node_vec.push_back(new Node(ptr->val));
            node_map[ptr] = i;
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