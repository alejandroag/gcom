from __future__ import division
import numpy as np
import matplotlib.pyplot as plt



def polynomial_curve_fitting(points, knots, method, L=0, libraries=False,
                             num_points=100, degree=None):    
    '''
       Fits planar curve to points at given knots. 

       Arguments:
           points -- coordinates of points to adjust (x_i, y_i) given by a numpy array of shape (N, 2)
           knots -- strictly increasing sequence at which the curve will fit the points, tau_i
               It is given by a np.array of shape N, unless knots='chebyshev', in this case
                   N Chebyshev's nodes between 0 and 1 will be used instead of tau.
           method -- one of the following: 
               'newton' computes the interpolating polynomial curve using Newton's method. 
               'least_squares' computes the best adjusting curve in the least square sense,
                   i.e., min_a ||Ca - b||**2 + L/2 ||a||**2
           L -- regularization parameter
           libraries -- If False, only numpy linear algebra operations are allowed. 
               If True, any module can be used. In this case, a very short and fast code is expected
           num_points -- number of points to plot between tau[0] and tau[-1]
           degree -- degree of the polynomial. Needed only if method='least_squares'.
                     If degree=None, the function will return the interpolating polynomial.

       Returns:
           numpy array of shape (num_points, 2) given by the evaluation of the polynomial
           at the evenly spaced num_points between tau[0] and tau[-1]
    '''

    if knots=='chebyshev': knots=chebyshev_knots(0, 1, points.shape[0])

    curve_x = polynomial_curve_fitting1d(points[:,0],knots,method,L,libraries,num_points,degree)
    curve_y = polynomial_curve_fitting1d(points[:,1],knots,method,L,libraries,num_points,degree)

    return np.array([curve_x,curve_y]).transpose()

def polynomial_curve_fitting1d(points, knots, method, L=0, libraries=False,
                             num_points=100, degree=None):    
    if method=='newton':
	return newton_polynomial(points,knots,num_points,libraries)


    elif method=='least_squares':
	return least_squares_fitting(points,knots,num_points,L,libraries,degree)

def newton_polynomial(x, tau, num_points=100, libraries=False):    
    #I've used polyfit and polyval if libraries==True
    #If you find something faster, I'll be glad to know about it.
    if not libraries: #Solo usamos librerias de algebra
        #your code here
        N = tau.size
        cache = np.zeros((N,N))
        cache[:,0] = x
        for i in range(N-1):
            cache[0:N-i-1,i+1] = (cache[1:N-i,i]-cache[0:N-i-1,i])/(1.0*(tau[i+1:N]-tau[0:N-i-1]))
            #print cache[0:N-i-1,i+1]
            #print tau[i+1:N]-tau[0:N-i-1]
            #print
        coefs = cache[0,:]
        #print coefs
        points = np.linspace(tau[0], tau[-1], num_points)
        polynomial = eval_poly(points,coefs,tau)     
        return polynomial #np.array of size num_points
    else: #Usamos cualquier libreria
        coefs = np.polyfit(tau,x,tau.size-1)
        points = np.linspace(tau[0], tau[-1], num_points)
        polynomial = np.polyval(coefs,points)

	#print polynomial
        return polynomial        
	#return another_polynomial #np.array of size num_points

def eval_poly(t, coefs, tau=None):    
    N = coefs.size
    if tau==None: tau=np.zeros(N)
    poly = coefs[-1]*np.ones(t.size)
    for i in range(2,N+1):
        poly = coefs[-i] + (t-tau[-i])*poly
    return poly
        
def least_squares_fitting(points, knots, num_points, L=0, libraries=True, degree=None):    
    #I've used np.linalg.lstsq and np.polyval if libraries==True

    if degree==None: degree=points.size-1

    if not libraries:
        m = points.size
        C = np.zeros((m,degree+1))
        C[:,0]=1
        for i in range(1,degree+1):
            C[:,i]=C[:,i-1]*knots

        H = np.dot(C.transpose(),C) + (L/2.0)*np.eye(degree+1)
        coefs = np.linalg.solve(H,np.dot(C.transpose(),points))
        t = np.linspace(knots[0], knots[-1], num_points)
        polynomial = eval_poly(t,coefs)
        return polynomial	

    else:
        C = np.vander(knots,degree+1)
        (coefs,_,_,_) = np.linalg.lstsq(C,points)
        t = np.linspace(knots[0], knots[-1], num_points)
        polynomial = np.polyval(coefs,t)
        return polynomial
        
def chebyshev_knots(a, b, n):
    t=np.arange(1,n+1)
    t=(a+b-(a-b)*np.cos((2*t-1)*np.pi/(2.0*n)))/2.0
    return t

