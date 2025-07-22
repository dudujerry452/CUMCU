import heapq
import numpy as np
from collections import defaultdict

# -- 核心修正：严格使用第五关附件中的所有参数 --
CONFIG = {
    "players": 2, "days_limit": 10, "weight_limit": 1200, "initial_cash": 10000,
    "mine_income": 200, "water_kg": 3, "food_kg": 2, "water_price": 5, "food_price": 10,
    "base_consumption": { "Sunny": {"water": 3, "food": 4}, "Hot": {"water": 9, "food": 9} },
    "weather": [None, "Sunny", "Hot", "Sunny", "Sunny", "Sunny", "Sunny", "Hot", "Hot", "Hot", "Hot"],
    "adj": {
        1: [2, 4, 5], 2: [1, 3, 4], 3: [2, 4, 8], 4: [1, 2, 3, 5, 7],
        5: [1, 4, 6], 6: [5, 7, 13], 7: [4, 5, 6, 12], 8: [3, 9],
        9: [8, 10, 11], 10: [9, 11], 11: [9, 10, 12], 12: [7, 11, 13], 13: [6, 12]
    },
    "start_node": 1, "end_node": 13, "mine_node": 9
}

def get_consumption(day, action):
    weather = CONFIG["weather"][day]
    base = CONFIG["base_consumption"][weather]
    w_consum, f_consum = base["water"], base["food"]
    multiplier = {"stay": 1, "move": 2, "mine": 3}.get(action, 1)
    return w_consum * multiplier, f_consum * multiplier

def find_k_best_paths(k):
    paths_pool = []
    penalty_on_edges = defaultdict(int)
    for _ in range(k):
        # -- 核心修正：寻路算法的目标是最小化金钱花费（花费-收入）--
        # 状态: (总金钱花费, day, pos, path)
        pq = [(0, 0, CONFIG["start_node"], [(0, CONFIG["start_node"])])] 
        visited = defaultdict(lambda: float('inf'))
        visited[(0, CONFIG["start_node"])] = 0
        best_path_found = None

        while pq:
            monetary_cost, day, pos, path = heapq.heappop(pq)
            if pos == CONFIG["end_node"] and day <= CONFIG["days_limit"]:
                final_path = path
                for stop_day in range(day + 1, CONFIG["days_limit"] + 1):
                    final_path.append((stop_day, pos))
                best_path_found = final_path
                break

            if monetary_cost > visited[(day, pos)] or day >= CONFIG["days_limit"]:
                continue

            next_day = day + 1
            possible_next_steps = [(pos, "stay")] + [(n, "move") for n in CONFIG["adj"].get(pos, [])]
            for next_pos, action_type in possible_next_steps:
                current_action = action_type
                if action_type == "stay" and pos == CONFIG["mine_node"]:
                    current_action = "mine"
                
                w_c, f_c = get_consumption(next_day, current_action)
                resource_cost = w_c * CONFIG['water_price'] + f_c * CONFIG['food_price']
                income = CONFIG['mine_income'] if current_action == 'mine' else 0
                
                # 新的成本函数：净金钱花费
                net_monetary_cost = resource_cost - income
                
                edge_penalty = penalty_on_edges.get((day, pos, next_pos), 0)
                new_total_cost = monetary_cost + net_monetary_cost + edge_penalty
                
                if new_total_cost < visited[(next_day, next_pos)]:
                    visited[(next_day, next_pos)] = new_total_cost
                    heapq.heappush(pq, (new_total_cost, next_day, next_pos, path + [(next_day, next_pos)]))
        
        if best_path_found:
            paths_pool.append(best_path_found)
            for i in range(len(best_path_found) - 1):
                d, p_curr = best_path_found[i]
                _, p_next = best_path_found[i+1]
                penalty_on_edges[(d, p_curr, p_next)] += 500 # 施加惩罚以寻找不同路径

    return paths_pool

def calculate_actual_consumption(path_self, path_opponent):
    total_w, total_f, total_income = 0, 0, 0
    for day in range(1, len(path_self)):
        pos_self, prev_pos_self = path_self[day][1], path_self[day-1][1]
        pos_opp, prev_pos_opp = path_opponent[day][1], path_opponent[day-1][1]
        
        action_self = "mine" if pos_self == CONFIG["mine_node"] and pos_self == prev_pos_self else ("move" if pos_self != prev_pos_self else "stay")
        action_opp = "mine" if pos_opp == CONFIG["mine_node"] and pos_opp == prev_pos_opp else ("move" if pos_opp != prev_pos_opp else "stay")

        move_collision = (action_self == "move" and action_opp == "move" and prev_pos_self == prev_pos_opp and pos_self == pos_opp)
        mine_collision = (action_self == "mine" and action_opp == "mine" and pos_self == pos_opp)
        
        w_c, f_c = get_consumption(day, action_self)
        income = CONFIG["mine_income"] if action_self == "mine" else 0

        if move_collision: w_c *= 2; f_c *= 2
        if mine_collision:
            base_cons = CONFIG["base_consumption"][CONFIG["weather"][day]]
            w_c, f_c = base_cons["water"] * 3, base_cons["food"] * 3
            income /= 2
        
        total_w += w_c; total_f += f_c; total_income += income
        
    return total_w, total_f, total_income

def calculate_payoff(path1, path2):
    w1, f1, income1 = calculate_actual_consumption(path1, path2)
    w2, f2, income2 = calculate_actual_consumption(path2, path1)
    payoffs = []
    for w, f, income in [(w1, f1, income1), (w2, f2, income2)]:
        cost = w * CONFIG["water_price"] + f * CONFIG["food_price"]
        weight = w * CONFIG["water_kg"] + f * CONFIG["food_kg"]
        
        if weight > CONFIG["weight_limit"] or cost > CONFIG["initial_cash"]:
            payoffs.append(-float('inf'))
        else:
            final_cash = CONFIG["initial_cash"] - cost + income
            payoffs.append(final_cash)
    return tuple(payoffs)

def solve_msne(payoff_matrix):
    k = len(payoff_matrix)
    A = np.zeros((k, k))
    for i in range(k - 1):
        for j in range(k):
            A[i, j] = payoff_matrix[i][j][0] - payoff_matrix[i + 1][j][0]
    A[k - 1, :] = 1
    b = np.zeros(k); b[k - 1] = 1
    try:
        probabilities = np.linalg.solve(A, b)
        return probabilities
    except np.linalg.LinAlgError:
        return None

def format_path_brief(path, path_id):
    w, f, income = calculate_actual_consumption(path, path)
    cost = w * CONFIG['water_price'] + f * CONFIG['food_price']
    final_cash = CONFIG['initial_cash'] - cost + income
    route = "->".join([str(p[1]) for p in path])
    return f"路径 {path_id}: 单人最终资金 {final_cash:.0f}元。路线概览: {route[:50]}..."

if __name__ == "__main__":
    K_PATHS = 2
    print(f"--- 第一步：寻找前 {K_PATHS} 条最优路径 (目标: 最大化资金) ---")
    path_pool = find_k_best_paths(K_PATHS)
    for i, p in enumerate(path_pool):
        print(format_path_brief(p, i + 1))

    print(f"\n--- 第二步：构建 {K_PATHS}x{K_PATHS} 支付矩阵 ---")
    payoff_matrix = [[(0,0) for _ in range(K_PATHS)] for _ in range(K_PATHS)]
    for i in range(K_PATHS):
        for j in range(K_PATHS):
            payoff_matrix[i][j] = calculate_payoff(path_pool[i], path_pool[j])
    
    print("支付矩阵 (玩家1收益, 玩家2收益):")
    header = "          " + "".join([f"  P2->路径{j+1}      " for j in range(K_PATHS)])
    print(header)
    for i in range(K_PATHS):
        row_str = f"P1->路径{i+1} "
        for j in range(K_PATHS):
            row_str += f"({payoff_matrix[i][j][0]:.0f}, {payoff_matrix[i][j][1]:.0f})   "
        print(row_str)

    print("\n--- 第三步：求解混合策略纳什均衡 ---")
    probabilities = solve_msne(payoff_matrix)

    if probabilities is not None and np.all(probabilities >= -1e-9):
        print("计算出的均衡策略概率为:")
        for i, prob in enumerate(probabilities):
            print(f"  - 选择 路径 {i+1} 的概率: {prob:.2%}")
        expected_payoff = np.dot(probabilities, [payoff_matrix[0][j][0] for j in range(K_PATHS)])
        print(f"\n在此均衡下，每位玩家的期望收益为: {expected_payoff:.2f} 元。")
        print("\n结论: 基于正确的地图数据和以最大化资金为目标的寻路算法，我们得到了最终的混合策略解。")
    else:
        print("无法计算出有效的混合策略纳什均衡。")
