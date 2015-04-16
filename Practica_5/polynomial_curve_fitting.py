from __future__ import division
import numpy as np
import matplotlib.pyplot as plt



def polynomial_curve_fitting(points, knots, method, L=0, libraries=False,
                             num_points=100):    
    '''
       Fits planar curve to points at given knots. 

       Arguments:
           points -- coordinates of points to adjust (x_i, y_i) given by a numpy array of shape (N, 2)
           knots -- strictly increasing sequence at which the curve will fit the points, tau_i
               It is given by a np.array of shape M, unless knots='chebyshev', in this case
                   N Chebyshev's nodes between 0 and 1 will be used instead of tau.
           method -- one of the following: 
               'newton' computes the interpolating polynomial curve using Newton's method.
                   returns error if N!=M. 
               'least_squares' computes the best adjusting curve in the least square sense,
                   i.e., min_a ||Ca - b||**2 + L/2 ||a||**2
           L -- regularization parameter
           libraries -- If False, only numpy linear algebra operations are allowed. 
               If True, any module can be used. In this case, a very short and fast code is expected
           num_points -- number of points to plot between tau[0] and tau[-1]

       Returns:
           numpy array of shape (num_points, 2) given by the evaluation of the polynomial
           at the evenly spaced num_points between tau[0] and tau[-1]
    '''

    curve_x = polynomial_curve_fitting1d(points[:,0],knots,method,L,libraries,num_points)
    curve_y = polynomial_curve_fitting1d(points[:,1],knots,method,L,libraries,num_points)

    return np.array([curve_x,curve_y]).transpose()

def polynomial_curve_fitting1d(points, knots, method, L=0, libraries=False,
                             num_points=100):    
    if method=='newton':
	return newton_polynomial(points,knots,num_points,libraries)


    elif method=='least_squares':
	return least_squares_fitting(points,knots,num_points,L,libraries)

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
        polynomial = coefs[N-1]
        for k in range(N-2,-1,-1):
            #print polynomial
            polynomial = coefs[k] + (points-tau[k])*polynomial
        
        #print polynomial     
        return polynomial #np.array of size num_points
    else: #Usamos cualquier libreria
        coefs = np.polyfit(tau,x,tau.size-1)
	points = np.linspace(tau[0], tau[-1], num_points)
	polynomial = np.polyval(coefs,points)

	#print polynomial
	return polynomial        
	#return another_polynomial #np.array of size num_points

def eval_poly(t, coefs, tau=None):    
    pass
        
def least_squares_fitting(points, knots, num_points, L=0, libraries=True):    
    #I've used np.linalg.lstsq and np.polyval if libraries==True

    if not libraries:
	k = points.size
	m = knots.size
	C = np.zeros((m,k))
	C[:,0]=1
	for i in range(1,k):
	    C[:,i]=C[:,i-1]*knots

	coefs = np.linalg.solve(C,points)
        polynomial = np.polyval(coefs,points)
        #t = np.linspace(knots[0], knots[-1], num_points)
        #polynomial = coefs[k-1]
        #for i in range(k-2,-1,-1):
        #    polynomial = coefs[i] + (t-knots[i])*polynomial

	return polynomial	

    else:
    	C = np.vander(knots,points.size,increasing=True)
	coefs = np.linalg.lstsq(C,points)
	polynomial = np.polyval(coefs,points)
        
def chebyshev_knots(a, b, n):
    pass
