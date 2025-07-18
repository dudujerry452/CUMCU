import numpy as np

def checkcol(p0, p1, p2, o, d): 
    norm_d = np.linalg.norm(d)
    if norm_d == 0:
        print("d is zero")
        return (False, 0)
    d = d / norm_d  # Normalize direction vector
    E1 = p1 - p0 
    E2 = p2 - p0
    T = o - p0 
    Fac = np.column_stack((-d, E1, E2)) 
    print("Fac:", Fac)
    try: 
        x = np.linalg.solve(Fac, T)
        print("x:", x)
        t,u,v = x[0],x[1],x[2]
        if t < 0 or u < 0 or v < 0 or u + v > 1: 
            return (False,t)
        else: 
            return (True, t)
    except np.linalg.LinAlgError as e: 
        return (False,t)
    
# 
    
def checksquare_mat(mat, o, d): 
    mat = mat.astype(np.float64)
    o = o.astype(np.float64)
    d = d.astype(np.float64)

    p0, p1, p2, p3 = mat[0], mat[1], mat[2], mat[3]
    r1 = checkcol(p0, p1, p2, o, d)
    r2 = checkcol(p0, p2, p3, o, d)
    if r1[0]: 
        return r1
    else:
        return r2
    
# def gene_rays(): 






def test():
    p0 = np.array([[5,0,0], [5,0,5], [5,5,5], [5,5,0]])
    dif = np.array([1,0,0])
    p1 = p0+dif
    p2 = p1+dif 

    ori = np.array([0,2.5,2.5])
    d = np.array([1,0,-1.0])

    print(checksquare_mat(p0, ori, d))
    print(checksquare_mat(p1, ori, d))
    print(checksquare_mat(p2, ori, d))


test()
