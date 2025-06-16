# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 18:59:14 2025

@author: MEGHNA
"""

## Projectile launched from surface of earth but all distances are
## measured from center of earth
## gravity force is variable

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sci

#constants
G = 6.67*10**-11  ##grav constant
Rp = 6357000 ##planet radius in m
mp = 5.972e24 ##planet mass in kg

##rocket
m = 640/1000  ##kg


def gravity(x,z):
    global Rp, mp
    
    r = np.sqrt(x**2 + z**2)
    
    if r< Rp:
        accx = 0.0
        accz = 0.0
    else:
        accx = G*mp/(r**3)*x
        accz = G*mp/(r**3)*z
    
    acc =  np.asarray([accx, accz])
    return acc
    
    
## Equations of motion
## F = m*a = m*zddot
# z = altitude from center of earth along north pole
# x = altitude from center of earth along equator
## zdot = velocity along z
## zddot = acceleration along z
def Derivatives(state,t):
    global m
    
    x = state[0]
    z =  state[1]
    velx = state[2]
    velz = state[3]
    
    #compute zdot and xdot
    xdot = velx
    zdot = velz
    
    #Compute all forces
    #gravity
    gravf = -gravity(x, z)*m
    
    #aerodynamic
    aerof = np.asarray([0.0,0.0])
    
    #thrust
    thrustf = np.asarray([0.0,0.0])
    
    F = gravf + aerof + thrustf
    
    #compute zddot
    ddot =  F/m
    
    #compute statedot
    statedot = np.asarray([xdot,zdot,ddot[0],ddot[1]])
    
    return statedot


#Surface Gravity
print("g = ", gravity(0, Rp))

##initial conditions
x0 = Rp #+600000  ##m
z0 = 0.0   ##m
r0 = np.sqrt(x0**2 + z0**2)
velx0 = 0.0   ##m/s
velz0 = np.sqrt(G*mp/r0)*1.1  #m/s
state_initial = np.asarray([x0, z0, velx0, velz0])


#time window
period = 2*np.pi/np.sqrt(G*mp)*r0**(3.0/2.0)*1.5
t_out = np.linspace(0,period,1000)
state_final = sci.odeint(Derivatives,state_initial, t_out)


###outputs
xout = state_final[:,0]
zout = state_final[:,1]
altitude = np.sqrt(xout**2 + zout**2)- Rp
velxout = state_final[:,2]
velzout = state_final[:,3]
velout = np.sqrt(velxout**2 + velzout**2)


theta=np.linspace(0, 2*np.pi, 100)
xp = Rp*np.sin(theta)
yp = Rp*np.cos(theta)


##plotting
#2D orbit
plt.figure()
plt.plot(xout, zout, 'r--', label = 'Rocket trajectory')
plt.plot(xout[0], zout[0], 'g.', markersize = 20)
plt.plot(xp, yp, 'b-', label = 'Earth Orbit')
plt.xlabel('x -->')
plt.ylabel('y -->')
plt.grid()
#plt.axis('equal')
plt.legend()

#Altitude plot
plt.figure()
plt.plot(t_out,altitude)
plt.xlabel('Time (s) -->')
plt.ylabel('Altitude (m) -->')
plt.grid()
plt.legend()

#Velocity Plot
plt.figure()
plt.plot(t_out,velout)
plt.xlabel('Time (s) -->')
plt.ylabel('Velocity (m/s) -->')
plt.grid()
plt.legend()













