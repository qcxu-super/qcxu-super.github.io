class MinStack {
public:
    /** initialize your data structure here. */
    MinStack() {

    }
    
    void push(int x) {
        _data.push(x);
        if (_min.empty()) {
            _min.push(x);
        } 
        else if (_min.top() >= x) {
            _min.push(x);
        }
        else {
            _min.push(_min.top());
        }
    }
    
    void pop() {
        _data.pop();
        _min.pop();
    }
    
    int top() {
        return _data.top();
    }
    
    int getMin() {
        return _min.top();
    }
private:
    std::stack<int> _data;
    std::stack<int> _min;
};