def pi_newton(n):
    r= 0
    r1= 1
    s= -1
    coefs =[]
    for k in range(n):
        s *= -1
        c  = (1/math.factorial(k))*r1*s(1/(2*k+1))
        r += c
        coefs.append(c)
        r1 *=(1/2-k)
        return 4*r,coefs