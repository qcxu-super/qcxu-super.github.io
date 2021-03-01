class Solution {
public:
    int calculate(string s) {
        std::stack<int> stk;
        int num = 0;
        bool num_is_valid = 0;
        for (int i=0; i<s.size(); ++i) {
            char c = s[i];

            if (c >= '0' && c <= '9') {
                num = num * 10 + (c - '0');
                num_is_valid = 1;

                if (i == s.size()-1) {
                    if (num_is_valid) {
                        stk.push(num);
                        num_is_valid = 0;
                    }
                }
            }
            else if (c == ' ' && i == s.size()-1 && num_is_valid == 1) {
                stk.push(num);
            }
            else if (c == '+' || c == '-') {
                if (num_is_valid) {
                    stk.push(num);
                    num = 0;
                    num_is_valid = 0;
                }
                if (c == '+') {
                    stk.push(1);
                }
                else if (c == '-') {
                    stk.push(-1);
                }
            }
            else if (c == '(') {
                stk.push(-999999);
            }
            else if (c == ')') {
                if (num_is_valid) {
                    stk.push(num);
                    num = 0;
                    num_is_valid = 0;
                }

                int res = 0;
                while(stk.top() != -999999) {
                    int numi = stk.top();
                    stk.pop();
                    int signi = 1;
                    if (!stk.empty() && stk.top() != -999999) {
                        signi = stk.top();
                        stk.pop();
                    }
                    res += signi * numi;
                }
                if (!stk.empty() && stk.top() == -999999) {
                    stk.pop();
                }
                stk.push(res);
            }
        }

        int res = 0;
        while (!stk.empty()) {
            int numi = stk.top();
            stk.pop();
            int signi = 1;
            if (!stk.empty() && stk.top() != -999999) {
                signi = stk.top();
                stk.pop();
            }
            res += signi * numi;
        }

        return res;
    }
};

