#include <vector>
#include <algorithm>
#include <queue>

bool cmp(const vector<int>& a, const vector<int>& b) {
    return a[0] < b[0];
}

class Solution {
public:
    int minRefuelStops(int target, int startFuel, vector<vector<int>>& stations) { // distance,fuelnum

        if (stations.size() == 0 && startFuel < target) {
            return -1;
        }

        std::sort(stations.begin(), stations.end(), cmp);

        std::priority_queue<int> big_heap;
        int result = 0;
        int total = target;

        // each station
        for (int i = 0; i < stations.size(); ++i) {
            int dist = stations[i][0]; // start--station
            int feul = stations[i][1];

            int distance = target - (total-dist); // start--station1--station2--end, target:station1--end, dist:start--station2, total:start--end
            
            startFuel -= distance;
            while (startFuel < 0) {
                if (big_heap.empty()) {
                    return -1;
                }
                startFuel += big_heap.top();
                big_heap.pop();
                ++result;
            }
            target -= distance;
            big_heap.push(feul);
        }

        // last_station--end
        if (target > 0) {
            startFuel -= target;
            while (startFuel < 0) {
                if (big_heap.empty()) {
                    return -1;
                }
                startFuel += big_heap.top();
                big_heap.pop();
                ++result;
            }
        }

        return result;
    }
};