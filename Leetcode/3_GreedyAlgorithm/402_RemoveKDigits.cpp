class Solution {
public:
    string removeKdigits(string num, int k) {
        std::vector<int> s;
        std::string result = "";
        for (int i=0; i<num.length(); ++i) {
            int number = num[i] - '0';
            while (s.size() != 0 && k > 0 && s[s.size()-1] > number) {
                s.pop_back();
                --k;
            }
            // number == 0
            if ((number==0 && s.size()>0) || number>0) {
                s.push_back(number);
            }
        }
        // k > 0
        while (s.size() > 0 && k > 0) {
            s.pop_back();
            --k;
        }
        // save result
        for (int i=0; i<s.size(); ++i) {
            result += '0' + s[i];
        }
        if (result == "") {
            result = "0";
        }
        return result;
    }
};