#include <vector>
#include <queue>

class Solution {
public:
    int findKthLargest(vector<int>& nums, int k) {
        std::priority_queue<int, std::vector<int>, std::greater<int> > q;
        for (int i=0; i<nums.size(); ++i) {
            if (q.size() < k) {
                q.push(nums[i]);
            }
            else if (q.top() < nums[i]) {
                q.pop();
                q.push(nums[i]);
            }
        }
        return q.top();
    }
};