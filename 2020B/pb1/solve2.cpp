#include <iostream> 
#include <stack>
#include <vector> 
#include <cstring>


using namespace std;
typedef pair<int, int> pr; 

const pr consume[3] = {{5,7}, {8,6}, {10,10}};
const pr mass = {3,2};
const pr price = {5,10};
const int limit = 1200; 
const int inital = 10000; 
const int profit = 1000; 
const int cost[31] = {0, 1, 1, 0, 2, 0, 1, 2, 0, 1, 1, 
                    2, 1, 0, 1, 1, 1, 2, 2, 1, 1, 
                    0, 0, 1, 0, 2, 1, 0, 0, 1, 1}; 

const int n = 14;
const int m = 30;

// 使用动态分配代替大数组
int ****dp;
struct Info {
    int p,d,i,j;
    void print() {printf("p:%d,d:%d,i:%d,j:%d\n",p,d,i,j);}
    void print(int pp) {printf("p:%d,d:%d,i:%d,j:%d,w:%d\n",p,d,i,j,pp);}
};
Info ****info;


std::vector<std::vector<int> > graph(20);  
void add(int a, int b) {graph[a].push_back(b); graph[b].push_back(a);}

// 内存分配函数
void allocateMemory() {
    // 分配 dp 数组
    dp = new int***[15];
    for(int i = 0; i < 15; i++) {
        dp[i] = new int**[31];
        for(int j = 0; j < 31; j++) {
            dp[i][j] = new int*[401];
            for(int k = 0; k < 401; k++) {
                dp[i][j][k] = new int[601];
                for(int l = 0; l < 601; l++) {
                    dp[i][j][k][l] = -1;
                }
            }
        }
    }
    
    // 分配 info 数组
    info = new Info***[15];
    for(int i = 0; i < 15; i++) {
        info[i] = new Info**[31];
        for(int j = 0; j < 31; j++) {
            info[i][j] = new Info*[401];
            for(int k = 0; k < 401; k++) {
                info[i][j][k] = new Info[601];
            }
        }
    }
}

void init() {
    allocateMemory();
    for(int i = 1; i <= 13; i ++) {
        add(i,i+1);
    }
    add(11,13);  // 节点11和13相连
    // 移除了原来的add(12,14)和add(11,14)
}

void solve() {

    // memset(dp, 0xff, sizeof(dp)); // 移除这行，因为我们在分配时已经初始化了

    for(int i = 0; i*mass.first <= limit; i ++) {
        for(int j = 0; i*mass.first + j*mass.second <= limit; j ++) {
            dp[1][0][i][j] = inital - i*price.first - j*price.second;
        }
    }

    for(int d = 1; d <= m; d ++) {

        cout << "d = " << d << endl;

        for(int p = 1; p <= n; p ++) {

    for(int i = 0; i*mass.first <= limit; i ++) {
        for(int j = 0; i*mass.first + j*mass.second <= limit; j ++) {
            Info ifo = info[p][d][i][j];
            int maxx = -1;
            pr c = consume[cost[d]]; 
            if(cost[d] != 2&&(i+2*c.first)*mass.first+(j+2*c.second)*mass.second <= limit) {
                for(auto x: graph[p]) {
                    int t = dp[x][d-1][i+2*c.first][j+2*c.second];
                    if(t > maxx) {
                        maxx = t; 
                        ifo.p = x; 
                        ifo.d = d-1; 
                        ifo.i = i + 2*c.first; 
                        ifo.j = j + 2*c.second;
                    }
                }
            }
            
            if ((i+c.first)*mass.first+(j+c.second)*mass.second <= limit&&dp[p][d-1][i+c.first][j+c.second] > maxx ) {
                maxx = dp[p][d-1][i+c.first][j+c.second];
                ifo.p = p; 
                ifo.d = d-1; 
                ifo.i = i + c.first; 
                ifo.j = j + c.second;
            }

            if(p == 8 || p == 11) {
                if((i+3*c.first)*mass.first+(j+3*c.second)*mass.second <= limit) {
                    int t = dp[p][d-1][i+3*c.first][j+3*c.second];
                    if(t >= 0) { 
                        t += profit; 
                        if(t > maxx ) {
                            maxx = t;
                            ifo.p = p; 
                            ifo.d = d-1; 
                            ifo.i = i+3*c.first; 
                            ifo.j = j+3*c.second;
                        }
                    }

                }
            }
            if(maxx < 0) break;

            dp[p][d][i][j] = maxx; 
            // if(i%20 == 0  j %20 == 0)
            // printf("dp[%d][%d][%d][%d] = %d\n", p,d,i,j,maxx);

        }
    }
    
    if(p == 9 || p == 12) {
        for(int i = 0; i*mass.first <= limit; i ++) {
            for(int j = 0; i*mass.first + j*mass.second <= limit; j ++) {
                Info ifo = info[p][d][i][j];
                int maxx = dp[p][d][i][j];

                    for(int i1 = i; i1 >= 0; i1 --) {
                        for(int j1 = j; j1 >= 0; j1 --) {
                            if(dp[p][d][i-i1][j-j1] < 0) break; 
                            int t = dp[p][d][i-i1][j-j1] - 2*price.first*i1 - 2*price.second*j1;
                            if(t < 0) continue; 
                            if(t > maxx) {
                                maxx = t; 
                                ifo.p = p; 
                                ifo.d = d; 
                                ifo.i = i-i1; 
                                ifo.j = j-j1;
                            }
                        }
                    }
                dp[p][d][i][j] = maxx;
                // printf("dp[%d][%d][%d][%d] = %d\n", p,d,i,j,maxx);
            }
        }
    }


        }
    }

    int maxi = 0, maxj = 0, maxans = dp[14][30][0][0]; 
    for(int i = 0; i*mass.first <= limit; i ++) {
        for(int j = 0; i*mass.first + j*mass.second <= limit; j ++) {
            if(dp[14][30][i][j] > maxans) {
                maxans = dp[14][30][i][j];
                maxi = i; 
                maxj = j; 
            }
        }
    }

    printf("i = %d, j = %d, ans = %d\n", maxi, maxj, dp[14][30][maxi][maxj]);
    Info cur= {14,30,maxi,maxj};

    while(cur.d > 0) {
        cur.print(dp[cur.p][cur.d][cur.i][cur.j]);
        cur = info[cur.p][cur.d][cur.i][cur.j];
    }
    cur.print(dp[cur.p][cur.d][cur.i][cur.j]);
    
}

int main() {

    init();
    solve();



    return 0; 
}
