#include <vector>
#include <queue>

class MedianFinder {
public:
    std::priority_queue<int, std::vector<int>, std::less<int> > big_heap;
    std::priority_queue<int, std::vector<int>, std::greater<int> > small_heap;
    
    MedianFinder() {
        
    }

    void addNum(int num) {
        if (big_heap.empty()) {
            big_heap.push(num);
            return;
        }
        // big_heap.size() == small_heap.size()
        if (big_heap.size() == small_heap.size() && num < small_heap.top()) {
            big_heap.push(num);
        }
        else if (big_heap.size() == small_heap.size() && num >= small_heap.top()) {
            small_heap.push(num);
        }
        // big_heap.size() < small_heap.size()
        else if (big_heap.size() < small_heap.size() && num >= small_heap.top()) {
            big_heap.push(small_heap.top());
            small_heap.pop();
            small_heap.push(num);
        }
        else if (big_heap.size() < small_heap.size() && num < small_heap.top()) {
            big_heap.push(num);
        }
        // big_heap.size() > small_heap.size(), small heap may be NULL
        else if (big_heap.size() > small_heap.size() && num > big_heap.top()) {
            small_heap.push(num);
        }
        else if (big_heap.size() > small_heap.size() && num <= big_heap.top()) {
            small_heap.push(big_heap.top());
            big_heap.pop();
            big_heap.push(num);
        }
    }

    double findMedian() {
        if (big_heap.size() == small_heap.size()) {
            return 1.0 * (big_heap.top() + small_heap.top())/2;
        }
        else if (big_heap.size() > small_heap.size()) {
            return big_heap.top();
        }
        else {
            return small_heap.top();
        }
    }
};

