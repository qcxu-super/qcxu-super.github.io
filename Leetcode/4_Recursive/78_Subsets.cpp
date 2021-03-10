// method 1
class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> result;
        vector<int> item;
        result.push_back(item);
        generate(0,nums,item,result);
        return result;
    }
private:
    void generate(int i, vector<int>& nums, vector<int>& item, vector<vector<int>>& result) {
        if (i >= nums.size()) {
            return;
        }
        item.push_back(nums[i]); // put nums[i]
        result.push_back(item);
        generate(i+1, nums, item, result);
        item.pop_back(); // not put nums[i]
        generate(i+1, nums, item, result);
    }
};


// method 2
class Solution {
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int>> result;
        int all_set = 1<<nums.size(); // 2^n. 0001<<3=1000=8=2^3
        for (int i=0; i<all_set; ++i) {
            vector<int> item;
            for (int j=0; j<nums.size(); ++j) {
                if (i & (1<<j)) { //0:001,1:010,2:100
                    item.push_back(nums[j]);
                }
            }
            result.push_back(item);
        }
        return result;
    }
};