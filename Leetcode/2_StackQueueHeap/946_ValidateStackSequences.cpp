#include <stack>
#include <queue>

class Solution {
public:
    bool validateStackSequences(vector<int>& pushed, vector<int> popped) {
        queue<int> s_popped;
        if (pushed.size() != popped.size()) {
            return false;
        }
        int n = pushed.size();
        for (int i=0; i<n; ++i) {
            s_popped.push(popped[i]);
        }

        stack<int> s;
        for (int i=0; i<n; ++i) {
            s.push(pushed[i]);
            while (!s.empty() && s.top() == s_popped.front()) {
                s.pop();
                s_popped.pop();
            }
        }
        if (s.empty()) {
            return true;
        }
        else {
            return false;
        }
    }
};