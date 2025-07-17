import sympy as sp
from sympy import symbols, cos, sin, solve, simplify, expand, sqrt

def solve_system_12():
    """
    用Python符号计算求解方程组(12)
    """
    print("用Python符号计算求解方程组(12):")
    print("(x3 - R)² + y3² = r3²")
    print("(x3 - R cos θ)² + (y3 - R sin θ)² = r3²")
    print("(R - R cos θ)² + (R sin θ)² = 2r3²(1 - cos 2α3)")
    print("="*60)
    
    # 定义符号变量
    x3, y3, r3_sq, R, theta, alpha3 = symbols('x3 y3 r3_sq R theta alpha3', real=True)
    
    # 定义方程组
    eq1 = (x3 - R)**2 + y3**2 - r3_sq
    eq2 = (x3 - R*cos(theta))**2 + (y3 - R*sin(theta))**2 - r3_sq
    eq3 = (R - R*cos(theta))**2 + (R*sin(theta))**2 - 2*r3_sq*(1 - cos(2*alpha3))
    
    print("\n方程组:")
    print(f"eq1: {eq1} = 0")
    print(f"eq2: {eq2} = 0")
    print(f"eq3: {eq3} = 0")
    
    # 求解方程组
    print("\n正在求解方程组...")
    
    try:
        # 求解完整的方程组
        solutions = solve([eq1, eq2, eq3], [x3, y3, r3_sq])
        
        print(f"\n找到 {len(solutions)} 个解:")
        
        for i, sol in enumerate(solutions):
            print(f"\n解 {i+1}:")
            print(f"x3 = {sol[0]}")
            print(f"y3 = {sol[1]}")
            print(f"r3² = {sol[2]}")
            
            # 简化解
            print(f"\n简化后:")
            print(f"x3 = {simplify(sol[0])}")
            print(f"y3 = {simplify(sol[1])}")
            print(f"r3² = {simplify(sol[2])}")
            
    except Exception as e:
        print(f"直接求解失败: {e}")
        print("尝试分步求解...")
        
        # 分步求解
        step_by_step_solve()

def step_by_step_solve():
    """
    分步求解方程组
    """
    print("\n" + "="*60)
    print("分步求解:")
    
    # 重新定义变量
    x3, y3, r3_sq, R, theta, alpha3 = symbols('x3 y3 r3_sq R theta alpha3', real=True)
    
    # 步骤1: 从方程3求解r3²
    print("\n步骤1: 从方程3求解r3²")
    eq3 = (R - R*cos(theta))**2 + (R*sin(theta))**2 - 2*r3_sq*(1 - cos(2*alpha3))
    
    # 简化方程3的左边
    left_side = (R - R*cos(theta))**2 + (R*sin(theta))**2
    left_simplified = simplify(left_side)
    print(f"方程3左边简化: {left_simplified}")
    
    # 求解r3²
    r3_sq_solution = solve(eq3, r3_sq)[0]
    print(f"r3² = {r3_sq_solution}")
    print(f"r3² 简化 = {simplify(r3_sq_solution)}")
    
    # 步骤2: 从方程1和2求解x3, y3
    print("\n步骤2: 从方程1和2求解x3, y3")
    eq1 = (x3 - R)**2 + y3**2 - r3_sq_solution
    eq2 = (x3 - R*cos(theta))**2 + (y3 - R*sin(theta))**2 - r3_sq_solution
    
    print("将r3²代入方程1和2...")
    
    # 求解x3, y3
    xy_solutions = solve([eq1, eq2], [x3, y3])
    
    print(f"\n找到 {len(xy_solutions)} 个(x3, y3)解:")
    
    for i, sol in enumerate(xy_solutions):
        print(f"\n解 {i+1}:")
        print(f"x3 = {sol[0]}")
        print(f"y3 = {sol[1]}")
        
        # 简化解
        print(f"\n简化后:")
        x3_simplified = simplify(sol[0])
        y3_simplified = simplify(sol[1])
        print(f"x3 = {x3_simplified}")
        print(f"y3 = {y3_simplified}")
        
        # 进一步简化
        print(f"\n进一步简化:")
        x3_expanded = simplify(expand(x3_simplified))
        y3_expanded = simplify(expand(y3_simplified))
        print(f"x3 = {x3_expanded}")
        print(f"y3 = {y3_expanded}")
    
    return xy_solutions, r3_sq_solution

def alternative_solve():
    """
    尝试替代求解方法
    """
    print("\n" + "="*60)
    print("替代求解方法:")
    
    x3, y3, r3_sq, R, theta, alpha3 = symbols('x3 y3 r3_sq R theta alpha3', real=True)
    
    # 方法1: 先消除r3²
    print("\n方法1: 先消除r3²")
    eq1 = (x3 - R)**2 + y3**2 - r3_sq
    eq2 = (x3 - R*cos(theta))**2 + (y3 - R*sin(theta))**2 - r3_sq
    
    # 从eq1和eq2消除r3²
    eq_diff = eq1 - eq2
    print(f"eq1 - eq2 = {eq_diff}")
    eq_diff_simplified = simplify(eq_diff)
    print(f"简化后: {eq_diff_simplified} = 0")
    
    # 求解这个简化的方程
    if eq_diff_simplified != 0:
        # 解出x3和y3之间的关系
        y3_in_terms_of_x3 = solve(eq_diff_simplified, y3)
        print(f"\ny3 用x3表示: {y3_in_terms_of_x3}")
        
        # 代入方程1
        if y3_in_terms_of_x3:
            for y3_expr in y3_in_terms_of_x3:
                print(f"\n使用 y3 = {y3_expr}")
                eq1_substituted = eq1.subs(y3, y3_expr)
                print(f"代入方程1: {eq1_substituted} = 0")
                
                x3_solutions = solve(eq1_substituted, x3)
                print(f"x3的解: {x3_solutions}")
                
                for x3_val in x3_solutions:
                    y3_val = y3_expr.subs(x3, x3_val)
                    print(f"\n当x3 = {simplify(x3_val)}时")
                    print(f"y3 = {simplify(y3_val)}")
    
    # 方法2: 使用参数方程
    print("\n方法2: 使用参数方程")
    # 观察到这是两个圆的交点问题
    print("这是两个圆的交点问题:")
    print("圆1: 圆心(R, 0), 半径r3")
    print("圆2: 圆心(R cos θ, R sin θ), 半径r3")
    
    # 两圆心之间的距离
    center_distance = sqrt((R - R*cos(theta))**2 + (0 - R*sin(theta))**2)
    center_distance_simplified = simplify(center_distance)
    print(f"两圆心距离: {center_distance_simplified}")
    
    # 从方程3得到r3²的表达式
    eq3 = (R - R*cos(theta))**2 + (R*sin(theta))**2 - 2*r3_sq*(1 - cos(2*alpha3))
    r3_sq_from_eq3 = solve(eq3, r3_sq)[0]
    print(f"从方程3得到: r3² = {simplify(r3_sq_from_eq3)}")

def verify_solutions():
    """
    验证求得的解
    """
    print("\n" + "="*60)
    print("验证解:")
    
    # 获取解
    xy_solutions, r3_sq_solution = step_by_step_solve()
    
    x3, y3, r3_sq, R, theta, alpha3 = symbols('x3 y3 r3_sq R theta alpha3', real=True)
    
    # 原方程
    eq1_orig = (x3 - R)**2 + y3**2 - r3_sq
    eq2_orig = (x3 - R*cos(theta))**2 + (y3 - R*sin(theta))**2 - r3_sq
    eq3_orig = (R - R*cos(theta))**2 + (R*sin(theta))**2 - 2*r3_sq*(1 - cos(2*alpha3))
    
    print(f"\n验证r3²解:")
    eq3_check = eq3_orig.subs(r3_sq, r3_sq_solution)
    print(f"方程3代入r3²后: {simplify(eq3_check)}")
    
    for i, (x3_val, y3_val) in enumerate(xy_solutions):
        print(f"\n验证解 {i+1}:")
        print(f"x3 = {x3_val}")
        print(f"y3 = {y3_val}")
        print(f"r3² = {r3_sq_solution}")
        
        # 代入原方程验证
        eq1_check = eq1_orig.subs([(x3, x3_val), (y3, y3_val), (r3_sq, r3_sq_solution)])
        eq2_check = eq2_orig.subs([(x3, x3_val), (y3, y3_val), (r3_sq, r3_sq_solution)])
        
        print(f"方程1验证: {simplify(eq1_check)}")
        print(f"方程2验证: {simplify(eq2_check)}")

if __name__ == "__main__":
    # 尝试直接求解
    solve_system_12()
    
    # 分步求解
    step_by_step_solve()
    
    # 替代方法
    alternative_solve()
    
    # 验证解
    verify_solutions()