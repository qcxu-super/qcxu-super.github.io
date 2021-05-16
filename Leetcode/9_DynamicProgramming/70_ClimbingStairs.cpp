# include <vector>

class Solution {
public:
    int climbStairs(int n) {
        std::vector<int> dp(n+3, 0);  // 如果n=0，前面两行就越界了，所以n+3
        dp[1] = 1;
        dp[2] = 2;
        for (int i=3; i<=n; ++i) {
            dp[i] = dp[i-1] + dp[i-2];
        }
        return dp[n];
    }
};