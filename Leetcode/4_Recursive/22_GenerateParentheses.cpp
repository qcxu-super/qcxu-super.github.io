class Solution {
public:
    vector<string> generateParenthesis(int n) {
        vector<string> result;
        generate("",n,n,result);
        return result;
    }

private:
    void generate(string item, int left, int right, vector<string>& result) {
        if (left == 0 && right == 0) {
            result.push_back(item);
            return;
        }
        if (left > 0) {
            generate(item+'(', left-1, right, result);
        }
        if (left < right) { // '(' is more then ')' in item
            generate(item+')', left, right-1, result);
        }
    }
};