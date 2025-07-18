import numpy as np
import math
import sympy as sp

from data import drone_x
from data import drone_y

def recv_angle(a,o,b): 
    xa = drone_x[a]
    ya = drone_y[a]
    xb = drone_x[b]
    yb = drone_y[b]
    xo = drone_x[o]
    yo = drone_y[o]

    print(f"{xa}, {ya}")
    print(f"{xo}, {yo}")
    print(f"{xb}, {yb}")
    
    vec1 = (xa - xo, ya - yo)
    vec2 = (xb - xo, yb - yo)


    angle_1 = math.atan2(vec1[1], vec1[0])
    angle_2 = math.atan2(vec2[1], vec2[0])
    print('angle1 = ', angle_1)
    print('angle2 = ', angle_2)

    angle_rad = abs(angle_1 - angle_2)
    
    if(angle_rad > math.pi): 
        angle_rad = 2*math.pi - angle_rad

    return angle_rad

# print(recv_angle(1,0,3)/math.pi*180)

def calc1(alp1, R): 
    x1 = R/2 
    r1 = (R*R)/(2*(1-np.cos(2*alp1)))
    y1 = np.sqrt(r1 - x1*x1)
    r1 = np.sqrt(r1)
    return (x1, y1, r1)

def calc1_1(alp1,R):
    x1=R/2
    y1=(R/2)*sp.cot(alp1)
    r=(R*R)/(2*(1-sp.cos(2*alp1)))
    r = sp.sqrt(r)
    x2=R/2
    y2=-(R/2)*sp.cot(alp1)
    
    solution1=(float (x1), float(y1), float(r))
    solution2=(float(x2), float(y2), float(r))

    #return (float (x1), float(y1), float(r))
    return (float(x2), float(y2), float(r))


def calc2(alp2, theta, R): 

    x2f1 = R/(2*np.cos(theta)*(1+np.tan(theta)**2))
    sin2alp = np.sin(alp2)**2 
    tan2alp = np.tan(alp2)**2
    sin2the = np.sin(theta)**2
    x2f2 = sin2the*tan2alp + sin2alp - sin2alp*tan2alp 
    x2f3 = sin2alp*sin2the*tan2alp
    x2 = x2f1*x2f2/x2f3
    y2 = R/(2*np.sin(theta)) - (R/(2*np.sin(theta)*(1+np.tan(theta)**2)))*(x2f2/x2f3)
    r2 = np.sqrt(R*R/(2*(1-np.cos(2*alp2))))

    return (x2,y2,r2)

def calc2_2(alpha, theta, R_val):
    
    # 第一组解
    x1 = R_val * (-1*sp.sin(theta) / sp.tan(alpha) + sp.cos(theta)) / 2
    y1 = R_val * (sp.sin(theta) + sp.cos(theta) / sp.tan(alpha)) / 2

    # 第二组解
    x2 = R_val * (sp.sin(theta) / sp.tan(alpha) + sp.cos(theta)) / 2
    y2 = R_val * (sp.sin(theta) - sp.cos(theta) / sp.tan(alpha)) / 2

    # 半径
    r_squared = R_val**2 / (4 * sp.sin(alpha)**2)
    r = sp.sqrt(r_squared)

    solution1=(float(x1.evalf()), float(y1.evalf()), float(r.evalf()))
    solution2=(float(x2.evalf()), float(y2.evalf()), float(r.evalf()))
    # 返回两组解（数值化）
    #return (float(x1.evalf()), float(y1.evalf()), float(r.evalf()))
    return  (float(x2.evalf()), float(y2.evalf()), float(r.evalf()))

def calc3(alp3, theta, R): 
    r3_2 = R*R*(1-np.cos(theta))/(1-np.cos(2*alp3))
    f1 = np.sin(theta)**2/(np.sin(theta)**2 + (1-np.cos(theta))**2)
    f2 = R + 2*(r3_2 - (R*R*(1-np.cos(theta))**2)/(np.sin(theta)**2) \
                + (r3_2*(1+np.cos(theta))**2)/(np.sin(theta)**2) \
                )
    x3 = f1*f2
    y3 = (1+np.cos(theta))/(np.sin(theta))*x3 
    r3 = np.sqrt(r3_2)

    return (x3,y3,r3)


def calc3_3(alpha, theta, R_val):
    # 用 sympy 的符号替代输入实参
    alpha = sp.sympify(alpha)
    theta = sp.sympify(theta)
    R = sp.sympify(R_val)

    # 第一组解
    x1 = R * (-sp.sin(theta) / sp.tan(alpha) + sp.cos(theta) + 1) / 2
    y1 = R * ((sp.cos(theta) - 1) *sp.cos(alpha) + sp.sin(theta)*sp.sin(alpha)) / (2 * sp.sin(alpha))

    # 第二组解
    x2 = R * (sp.sin(theta) / sp.tan(alpha) + sp.cos(theta) + 1) / 2
    y2 = -R * ((sp.cos(theta) - 1) *sp.cos(alpha) + sp.sin(theta)*sp.sin(alpha)) / (2 * sp.sin(alpha))
    
    # 第三组解
    x3 = R * (sp.sin(theta) / sp.tan(alpha) + sp.cos(theta) + 1) / 2
    y3 = -R * ((sp.cos(theta) - 1) *sp.cos(alpha) - sp.sin(theta)*sp.sin(alpha)) / (2 * sp.sin(alpha))
    
    # r² 的表达式
    r_squared = R**2 * (1 - sp.cos(theta)) / (1 - sp.cos(2 * alpha))
    r = sp.sqrt(r_squared)

    solution1=(float(x1.evalf()), float(y1.evalf()), float(r.evalf()))
    solution2=(float(x2.evalf()), float(y2.evalf()), float(r.evalf()))
    solutoin3=(float(x3.evalf()), float(y3.evalf()), float(r.evalf()))


    # 返回两组解（都是 r² 正的）
    return (float(x1.evalf()), float(y1.evalf()), float(r.evalf()))
    #return  (float(x2.evalf()), float(y2.evalf()), float(r.evalf()))
    #return (float(x3.evalf()), float(y3.evalf()), float(r.evalf()))

def solve(O, A, B, C): # A is the drone to be measuer 
    alp1 = recv_angle(B,A,O)
    alp2 = recv_angle(C,A,O)
    alp3 = recv_angle(C,A,B)
    theta = recv_angle(B,O,C)


    R = 100

    ret = []
    ret.append(calc1_1(alp1, R))
    ret.append(calc2_2(alp2, theta, R))
    ret.append(calc3_3(alp3, theta, R))

    return ret


solve(0, 2, 3, 1)
