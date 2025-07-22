#include <iostream> 
#include <stack>
#include <vector> 


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

const int n = 12;
const int m = 30;

int dp[13][31][401][601];

struct Info {
    int p,d,i,j;
    void print() {printf("p:%d,d:%d,i:%d,j:%d\n",p,d,i,j);}
    void print(int pp) {printf("p:%d,d:%d,i:%d,j:%d,w:%d\n",p,d,i,j,pp);}
}info[13][31][401][601];


std::vector<std::vector<int> > graph(20);  
void add(int a, int b) {graph[a].push_back(b); graph[b].push_back(a);}

void init() {
    add(1,2);add(2,3);add(3,4);add(4,5);add(5,6);add(6,7);
    add(7,8);add(8,9);
    add(7,10);add(10,11);add(11,12);
}

void solve() {

    memset(dp, 0xff, sizeof(dp));

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
            Info& ifo = info[p][d][i][j];
            int maxx = -1;
            pr c = consume[cost[d]]; 
            if(cost[d] != 2 && (i+2*c.first)*mass.first+(j+2*c.second)*mass.second <= limit) {
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
            
            if ((i+c.first)*mass.first+(j+c.second)*mass.second <= limit && dp[p][d-1][i+c.first][j+c.second] > maxx ) {
                maxx = dp[p][d-1][i+c.first][j+c.second];
                ifo.p = p; 
                ifo.d = d-1; 
                ifo.i = i + c.first; 
                ifo.j = j + c.second;
            }

            if(p == 9) {
                if((i+3*c.first)*mass.first+(j+3*c.second)*mass.second <= limit)  {
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
            // if(i%20 == 0 && j %20 == 0)
            // printf("dp[%d][%d][%d][%d] = %d\n", p,d,i,j,maxx);

        }
    }
    
    if(p == 7) {
        for(int i = 0; i*mass.first <= limit; i ++) {
            for(int j = 0; i*mass.first + j*mass.second <= limit; j ++) {
                Info& ifo = info[p][d][i][j];
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

    int maxi = 0, maxj = 0, maxans = dp[12][30][0][0]; 
    for(int i = 0; i*mass.first <= limit; i ++) {
        for(int j = 0; i*mass.first + j*mass.second <= limit; j ++) {
            if(dp[12][30][i][j] > maxans) {
                maxans = dp[12][30][i][j];
                maxi = i; 
                maxj = j; 
            }
        }
    }

    printf("i = %d, j = %d, ans = %d\n", maxi, maxj, dp[12][30][maxi][maxj]);
    Info cur= {12,30,maxi,maxj};

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
