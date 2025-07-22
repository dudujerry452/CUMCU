#include <iostream> 
#include <vector> 
#include <string>
#include <iomanip>
#include <algorithm>
#include <locale>
using namespace std; 
typedef pair<int, int> pr;

const pr cost[3] = {{3,4}, {9,9}, {10,10}};  // 晴朗、高温、沙暴的消耗
const pr mass = {3,2};
const int price[] = {5,10};
const int limit = 1200; 
const int inital = 10000; 
const int profit = 200; 
const float disturb[2] = {0.5,0.5};  // 天气概率：晴朗0.5，高温0.5

vector<int> graph[26]; 
void add(int a, int b) {graph[a].push_back(b); graph[b].push_back(a);}

float v[9][11][400][600];

// 存储最优策略：对于每个状态，记录最优动作
struct Policy {
    int next_pos;    // 下一个位置
    int action_type; // 0: 移动, 1: 停留
    bool is_valid;
    
    Policy() : next_pos(-1), action_type(-1), is_valid(false) {}
    Policy(int pos, int act) : next_pos(pos), action_type(act), is_valid(true) {}
};

Policy policy[9][11][400][600];

struct Info {
int p,d;
void print() {
printf("p = %d, d = %d\n", p,d);
}
}info [9][11][400][600];

void init() {
add(1,2); add(2,3); add(3,4);
add(1,5);add(5,6);add(6,7);add(7,8);add(8,4);
}

void solve () {

cout << "开始求解MDP..." << endl;

// 初始化策略和值函数
for(int p = 1; p <= 8; p++) {
    for(int d = 0; d <= 10; d++) {
        for(int w = 0; w < 400; w++) {
            for(int f = 0; f < 600; f++) {
                policy[p][d][w][f] = Policy();
                v[p][d][w][f] = -10000; // 初始化为很小的值
            }
        }
    }
}

cout << "初始化完成，设置边界条件..." << endl;

// 边界条件：第10天在终点4的价值
int boundary_count = 0;
for(int w = 0; w*mass.first <= limit&&w < 400; w ++) {
    for(int f = 0; w * mass.first + f*mass.second <= limit&&f < 600; f ++) {
        v[4][10][w][f] = w*0.5*price[0] + f*0.5*price[1];
        boundary_count++;
    }
}

cout << "边界条件设置完成，共" << boundary_count << "个状态" << endl;

for(int d = 9; d >= 1; d --) {
    cout << "d = " << d << endl;

    for(int p = 1; p <= 8; p ++) {

        for(int w = 0; w*mass.first <= limit&&w < 400; w ++) {
            for(int f = 0; w * mass.first + f*mass.second <= limit&&f < 600; f ++) {

                Info ifo = info[p][d][f][w];
                Policy pol = policy[p][d][w][f];

                float maxx = -10000;
                int best_next_pos = -1;
                int best_action = -1;
                
                // 尝试移动到相邻位置
                for(auto x : graph[p]) {
                    float newv[2] = {0,0}, newv_s = 0;
                    for(int ll = 0; ll < 2; ll ++) {
                        int new_w = w - 2*cost[ll].first;
                        int new_f = f - 2*cost[ll].second;
                        if(new_w < 0 || new_f < 0 || new_w >= 400 || new_f >= 600) {
                            newv[ll] = -10000; 
                        } else {
                            newv[ll] = v[x][d+1][new_w][new_f];
                        }
                        newv_s += newv[ll] * disturb[ll];
                    }
                    if(newv_s > maxx) {
                        maxx = newv_s; 
                        ifo = {x, d+1};
                        best_next_pos = x;
                        best_action = 0; // 移动
                    }
                }

                // 尝试停留在原地
                {
                    float newv[2] = {0,0}, newv_s = 0; 
                    for(int ll = 0; ll < 2; ll ++) {
                        int new_w = w - cost[ll].first;
                        int new_f = f - cost[ll].second;
                        if(new_w < 0 || new_f < 0 || new_w >= 400 || new_f >= 600) {
                            newv[ll] = -10000; 
                        } else {
                            newv[ll] = v[p][d+1][new_w][new_f];
                        }
                        newv_s += newv[ll] * disturb[ll];
                    }

                    if(newv_s > maxx) {
                        maxx = newv_s; 
                        ifo = {p, d+1};
                        best_next_pos = p;
                        best_action = 1; // 停留
                    }
                }

                v[p][d][w][f] = maxx;
                pol = Policy(best_next_pos, best_action);
            }
        }
    }
}


float maxx = -1, ww, ff;
for(int w = 0; w*mass.first <= limit&&w < 400; w ++) {
    for(int f = 0; w * mass.first + f*mass.second <= limit&&f < 600; f ++) {
        v[1][0][w][f] = 10000 + v[1][1][w][f] - (w*price[0] + f*price[1]);
        if(v[1][0][w][f] > maxx) {
            maxx = v[1][0][w][f];
            ww =w, ff = f;
        }
    }
}

    cout << "最优期望价值: " << maxx << ", 最优初始购买: 水=" << ww << "箱, 食物=" << ff << "箱" << endl;
}

// 测试给定天气序列下的策略表现
float testPolicy(vector<int> weather_sequence, int init_w, int init_f) {
    int pos = 1;
    int day = 1;
    int water = init_w;
    int food = init_f;
    float money = inital - init_w * price[0] - init_f * price[1];
    
    cout << "\n=== 策略测试 ===" << endl;
    cout << "初始状态: 位置=" << pos << ", 水=" << water << ", 食物=" << food << ", 资金=" << money << endl;
    
    while(day <= 10) {
        if(pos == 4) {
            // 到达终点，退回剩余资源
            money += water * 0.5 * price[0] + food * 0.5 * price[1];
            cout << "第" << day-1 << "天到达终点，最终资金: " << money << endl;
            return money;
        }
        
        // 获取当前状态的最优策略
        if(water >= 400 || food >= 600 || !policy[pos][day][water][food].is_valid) {
            cout << "第" << day << "天: 状态无效或资源耗尽" << endl;
            return -1; // 失败
        }
        
        Policy pol = policy[pos][day][water][food];
        int weather = weather_sequence[day-1]; // 天气：0=晴朗，1=高温
        
        cout << "第" << day << "天: 位置=" << pos << ", 天气=" << (weather==0?"晴朗":"高温") 
             << ", 水=" << water << ", 食物=" << food;
        
        // 执行动作
        int next_pos = pol.next_pos;
        int consume_multiplier = (pol.action_type == 0) ? 2 : 1; // 移动消耗2倍，停留消耗1倍
        
        int water_consume = cost[weather].first * consume_multiplier;
        int food_consume = cost[weather].second * consume_multiplier;
        
        if(water < water_consume || food < food_consume) {
            cout << " -> 资源不足，游戏失败!" << endl;
            return -1;
        }
        
        water -= water_consume;
        food -= food_consume;
        pos = next_pos;
        
        cout << " -> " << (pol.action_type == 0 ? "移动到" : "停留在") << pos 
             << ", 消耗水=" << water_consume << ", 食物=" << food_consume << endl;
        
        day++;
    }
    
    // 10天结束但未到达终点
    cout << "10天结束未到达终点，游戏失败!" << endl;
    return -1;
}

// 生成所有可能的10天天气序列并测试
void testAllWeatherSequences(int init_w, int init_f) {
    cout << "\n=== 测试所有可能的天气序列 ===" << endl;
    
    vector<float> results;
    int total_sequences = 1024; // 2^10
    int success_count = 0;
    float total_success_money = 0;
    
    for(int seq = 0; seq < total_sequences; seq++) {
        vector<int> weather(10);
        int temp = seq;
        for(int i = 0; i < 10; i++) {
            weather[i] = temp % 2;
            temp /= 2;
        }
        
        cout << "\n天气序列 " << seq+1 << ": ";
        for(int i = 0; i < 10; i++) {
            cout << (weather[i] == 0 ? "晴" : "热");
        }
        
        float result = testPolicy(weather, init_w, init_f);
        if(result > 0) {
            results.push_back(result);
            success_count++;
            total_success_money += result;
        }
        
        if(seq < 10 || seq % 100 == 0) { // 只显示前几个和每100个的结果
            cout << " -> 结果: " << (result > 0 ? to_string(result) : "失败") << endl;
        }
    }
    
    cout << "\n=== 统计结果 ===" << endl;
    cout << "成功序列数: " << success_count << "/" << total_sequences << endl;
    cout << "成功率: " << (float)success_count / total_sequences * 100 << "%" << endl;
    
    if(success_count > 0) {
        cout << "平均成功资金: " << total_success_money / success_count << endl;
        
        // 找最好和最坏结果
        float best = *max_element(results.begin(), results.end());
        float worst = *min_element(results.begin(), results.end());
        cout << "最好结果: " << best << endl;
        cout << "最坏结果: " << worst << endl;
    }
}




int main() {
    
    init();
    solve();
    
    // 找到最优初始策略
    float best_value = -1;
    int best_w = 0, best_f = 0;
    
    for(int w = 0; w*mass.first <= limit&&w < 400; w ++) {
        for(int f = 0; w * mass.first + f*mass.second <= limit&&f < 600; f ++) {
            float value = 10000 + v[1][1][w][f] - (w*price[0] + f*price[1]);
            if(value > best_value) {
                best_value = value;
                best_w = w;
                best_f = f;
            }
        }
    }
    
    cout << "最优策略: 初始购买水=" << best_w << "箱, 食物=" << best_f << "箱" << endl;
    cout << "期望价值: " << best_value << endl;
    
    // 测试几个特定的天气序列
    cout << "\n=== 测试特定天气序列 ===" << endl;
    
    // 全晴朗
    vector<int> all_sunny = {0,0,0,0,0,0,0,0,0,0};
    cout << "\n全晴朗天气:";
    for(int w : all_sunny) cout << (w==0?"晴":"热");
    testPolicy(all_sunny, best_w, best_f);
    
    // 全高温
    vector<int> all_hot = {1,1,1,1,1,1,1,1,1,1};
    cout << "\n全高温天气:";
    for(int w : all_hot) cout << (w==0?"晴":"热");
    testPolicy(all_hot, best_w, best_f);
    
    // 交替天气
    vector<int> alternate = {0,1,0,1,0,1,0,1,0,1};
    cout << "\n交替天气:";
    for(int w : alternate) cout << (w==0?"晴":"热");
    testPolicy(alternate, best_w, best_f);
    
    // 如果想测试所有序列（可能很慢），取消下面注释
    // testAllWeatherSequences(best_w, best_f);
    
    return 0;
}
