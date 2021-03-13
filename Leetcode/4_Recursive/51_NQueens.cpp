class Solution {
public:
    vector<vector<string>> solveNQueens(int n) {
        vector<vector<string>> result; // [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
        vector<string> location; // [".Q..","...Q","Q...","..Q."]
        vector<vector<int>> mark; // [[1,1,1,1],[1,1,0,0],[1,0,1,0],[1,0,0,1]]]
        // init mark
        for (int i=0; i<n; ++i) {
            vector<int> m;
            for (int j=0; j<n; ++j) {
                m.push_back(0);
            }
            mark.push_back(m);
        }
        // init location
        for (int i=0; i<n; ++i) {
            string s = "";
            for (int j=0; j<n; ++j) {
                s.append(".");
            }
            location.push_back(s);
        }
        // put queen
        generate(0,n,location,result,mark);
        return result;
    }
private:
    void put_down_the_queen(int x, int y, vector<vector<int>>& mark) {
        static const int dx[] = {-1,1,0,0,-1,-1,1,1};
        static const int dy[] = {0,0,-1,1,-1,1,-1,1};
        mark[x][y] = 1;
        for (int i=0; i<mark.size(); ++i) { // max delta is mark.size()
            for (int j=0; j<8; ++j) { // iteration on direction
                int new_x = x + i * dx[j];
                int new_y = y + i * dy[j];
                if (new_x >= 0 && new_x < mark.size() && new_y >= 0 && new_y < mark.size()) {
                    mark[new_x][new_y] = 1;
                }
            }
        }
    }

    void generate(int i, int n, vector<string>& location, vector<vector<string>>& result, vector<vector<int>>& mark) {
        if (i == n) {
            result.push_back(location);
            return;
        }
        for (int j=0; j<n; ++j) {
            if (mark[i][j] == 0) {
                vector<vector<int>> tmp_mark = mark;
                location[i][j] = 'Q';
                put_down_the_queen(i,j,mark);
                generate(i+1, n, location, result, mark);
                mark = tmp_mark;
                location[i][j] = '.';
            }
        }
    }
};