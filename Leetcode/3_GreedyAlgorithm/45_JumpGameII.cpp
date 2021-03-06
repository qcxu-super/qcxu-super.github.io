class Solution {
public:
    int jump(std::vector<int>& nums) {
        int step = 0;
        for (int i = 0; i < nums.size()-1; ++i) { // the last one does not need to jump
            if (i+nums[i] >= nums.size()-1) { // [2,3,1], 0+2=2
                ++step;
                break;
            }
            int max_step = nums[i];
            int expect_max_index = i;
            int expect_current_index = i;
            int best_index = i;
            for (int idx = i + 1; idx <= i + max_step && idx < nums.size(); ++idx) {
                expect_current_index = idx + nums[idx];
                if (expect_current_index >= expect_max_index) {
                    expect_max_index = expect_current_index;
                    best_index = idx;
                }
            }
            i = best_index - 1; // because next ++i
            ++step;
        }
        return step; 
    }
};