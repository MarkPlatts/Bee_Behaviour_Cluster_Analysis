#!/usr/bin/python

from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg
from random import random

class EllipsoidTool:
    """Some stuff for playing with ellipsoids"""
    def __init__(self): pass
    
    def getMinVolEllipse(self, P=None, tolerance=0.01):
        """ Find the minimum volume ellipsoid which holds all the points
        
        Based on work by Nima Moshtagh
        http://www.mathworks.com/matlabcentral/fileexchange/9542
        and also by looking at:
        http://cctbx.sourceforge.net/current/python/scitbx.math.minimum_covering_ellipsoid.html
        Which is based on the first reference anyway!
        
        Here, P is a numpy array of N dimensional points like this:
        P = [[x,y,z,...], <-- one point per line
             [x,y,z,...],
             [x,y,z,...]]
        
        Returns:
        (center, radii, rotation)
        
        """
        (N, d) = np.shape(P)
        d = float(d)
    
        # Q will be our working array
        Q = np.vstack([np.copy(P.T), np.ones(N)]) 
        QT = Q.T
        
        # initializations
        err = 1.0 + tolerance
        u = (1.0 / N) * np.ones(N)

        # Khachiyan Algorithm
        while err > tolerance:
            V = np.dot(Q, np.dot(np.diag(u), QT))
            M = np.diag(np.dot(QT , np.dot(linalg.inv(V), Q)))    # M the diagonal vector of an NxN matrix
            j = np.argmax(M)
            maximum = M[j]
            step_size = (maximum - d - 1.0) / ((d + 1.0) * (maximum - 1.0))
            new_u = (1.0 - step_size) * u
            new_u[j] += step_size
            err = np.linalg.norm(new_u - u)
            u = new_u

        # center of the ellipse 
        center = np.dot(P.T, u)
    
        # the A matrix for the ellipse
        A = linalg.inv(
                       np.dot(P.T, np.dot(np.diag(u), P)) - 
                       np.array([[a * b for b in center] for a in center])
                       ) / d
                       
        # Get the values we'd like to return
        U, s, rotation = linalg.svd(A)
        radii = 1.0/np.sqrt(s)
        
        return (center, radii, rotation)

    def getEllipsoidVolume(self, radii):
        """Calculate the volume of the blob"""
        return 4./3.*np.pi*radii[0]*radii[1]*radii[2]

    def plotEllipsoid(self, center, radii, rotation, ax=None, plotAxes=False, cageColor='b', cageAlpha=0.2):
        """Plot an ellipsoid"""
        make_ax = ax == None
        if make_ax:
            fig = plt.figure()
            ax = fig.add_subplot(111)
            #ax = fig.add_subplot(111, projection='3d')
            
        u = np.linspace(0.0, 2.0 * np.pi, 100)
        v = np.linspace(0.0, np.pi, 100)
        
        # cartesian coordinates that correspond to the spherical angles:
        x = radii[0] * np.outer(np.cos(u), np.sin(v))
        y = radii[1] * np.outer(np.sin(u), np.sin(v))
        #z = radii[2] * np.outer(np.ones_like(u), np.cos(v))
        # rotate accordingly
        for i in range(len(x)):
            for j in range(len(x)):
                #[x[i,j],y[i,j],z[i,j]] = np.dot([x[i,j],y[i,j],z[i,j]], rotation) + center
                [x[i,j],y[i,j]] = np.dot([x[i,j],y[i,j]], rotation) + center
    
        if plotAxes:
            # make some purdy axes
            axes = np.array([[radii[0],0.0],
                             [0.0,radii[1]]])
                             #[0.0,0.0,radii[2]]])
            # rotate accordingly
            for i in range(len(axes)):
                axes[i] = np.dot(axes[i], rotation)
    
    
            # plot axes
            for p in axes:
                X3 = np.linspace(-p[0], p[0], 100) + center[0]
                Y3 = np.linspace(-p[1], p[1], 100) + center[1]
               # Z3 = np.linspace(-p[2], p[2], 100) + center[2]
                #ax.plot(X3, Y3, color=cageColor)
                #ax.plot(X3, Y3, Z3, color=cageColor)
    
        # plot ellipsoid
        #ax.plot_wireframe(x, y,  0, rstride=4, cstride=4, color=cageColor, alpha=cageAlpha)
        #ax.plot(x[0], y[0])        
        
        if make_ax:
            plt.show()
            plt.close(fig)
            del fig
        
if __name__ == "__main__":
    # make 100 random points

    min_rand_x = random()*100
    max_rand_x = min_rand_x + random()*(100-min_rand_x)
    min_rand_y = random()*100
    max_rand_y = min_rand_y + random()*(100-min_rand_y)
    
    n_random_points = 4

    random_x = [min_rand_x + (max_rand_x-min_rand_x)*random() for i in range(n_random_points)]
    random_y = [min_rand_x + (max_rand_x-min_rand_x)*random() for i in range(n_random_points)]    
    
    P = np.array([random_x,random_y]).T

    #P = np.reshape([random()*100 for i in range(20)],(10,2))

    # find the ellipsoid
    ET = EllipsoidTool()
    (center, radii, rotation) = ET.getMinVolEllipse(P, .01)

    fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    ax = fig.add_subplot(111)

    # plot points
    ax.scatter(P[:,0], P[:,1], color='g', marker='*', s=10)

    # plot ellipsoid
    #ET.plotEllipsoid(center, radii, rotation, ax=ax, plotAxes=True)
#    x_ellipse=[]
#    y_ellipse=[]
#    k = [x*0.01 for x in range(1,101)]
#    rads = [i * 2 * math.pi for i in k]
#    for iRad in rads:
#        x_ellipse.append(radii[1]*math.cos(iRad))
#        y_ellipse.append(radii[0]*math.sin(iRad))
#
#
#    
#    coords = np.array([np.array(x_ellipse), np.array(y_ellipse)]).T
#    
#    #coords_rotated = np.dot(coords, rotation)
#    #rotation[0,0]*x_centred + rotation[0,1]*y_centred
#    
#    x_centred = [i + coords[:,0] for i in x_ellipse]
#    y_centred = [i + coords[:,1] for i in y_ellipse]
    
    u = np.linspace(0.0, 2.0 * np.pi, 100)
    v = np.linspace(0.0, np.pi, 100)
        
    # cartesian coordinates that correspond to the spherical angles:
    x = radii[0] * np.outer(np.cos(u), np.sin(v))
    y = radii[1] * np.outer(np.sin(u), np.sin(v))
    #z = radii[2] * np.outer(np.ones_like(u), np.cos(v))
    # rotate accordingly
    for i in range(len(x)):
        for j in range(len(x)):
            #[x[i,j],y[i,j],z[i,j]] = np.dot([x[i,j],y[i,j],z[i,j]], rotation) + center
            [x[i,j],y[i,j]] = np.dot([x[i,j],y[i,j]], rotation) + center
    
    
    plt.plot(x,y, lw=0.01)
    plt.axis([0,100,0,100])
    plt.show()
    

    plt.close(fig)
    del fig