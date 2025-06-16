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


def gravity(z):
    global Rp, mp
    
    r = np.sqrt(z**2)
    
    if r< Rp:
        acc = 0.0;
    else:
        acc = G*mp/(r**3)*r
    
    return acc
    
    
## Equations of motion
## F = m*a = m*zddot
# z = altitude of the surface
## zdot = velocity
## zddot = acceleration
def Derivatives(state,t):
    global m
    z =  state[0]
    velz = state[1]
    
    #compute zdot
    zdot = velz
    
    #Compute all forces
    #gravity
    gravf = -gravity(z)*m
    
    #aerodynamic
    aerof = 0.0
    
    #thrust
    thrustf = 0.0
    
    F = gravf + aerof + thrustf
    
    #compute zddot
    zddot =  F/m
    
    #compute statedot
    statedot = np.asarray([zdot,zddot])
    
    return statedot


#Surface Gravity
print("g = ", gravity(Rp))

##initial conditions
z0 = Rp  ##m
velz0 = 1640  ##m/s
state_initial = np.asarray([z0, velz0])


#time window
t_out = np.linspace(0,345,1000)
state_final = sci.odeint(Derivatives,state_initial, t_out)


###outputs
zout = state_final[:,0]
altitude = zout - Rp
velzout = state_final[:,1]

##maximum altitude
max_alt = np.max(altitude)
print("Maximum Altitude reached = ", max_alt,"m")

## max_alt = velz0^2 sin^2 theta/2g
## => velz0 sin theta = sqrt(2g*max_alt)
## at max_alt velz0 sin theta - gt = 0 
## => t = velz0 sin theta/g
## => t = sqrt(2g*max_alt)/g = sqrt(2*max_alt/g)


#total time of flight
t_tot = 2*np.sqrt(2*max_alt/gravity(Rp))
print("Total Time of Flight = ",t_tot, "secs")


##plotting
#Altitude plot
plt.figure()
plt.plot(t_out,altitude, label = 'trajectory')
plt.xlabel('Time (s) -->')
plt.ylabel('Altitude (m) -->')
plt.grid()
plt.legend()

#Velocity Plot
plt.figure()
plt.plot(t_out,velzout, label = 'velocity')
plt.xlabel('Time (s) -->')
plt.ylabel('Normal Speed (m/s) -->')
plt.grid()
plt.legend()














