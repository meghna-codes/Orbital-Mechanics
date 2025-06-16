# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 18:59:14 2025

@author: MEGHNA
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as sci

#constants
m = 640/1000 ##kg


## Equations of motion
## F = m*a = m*zddot
# z = altitude of the surface
## zdot = velocity
## zddot = acceleration
def Derivatives(state,t):
    z =  state[0]
    velz = state[1]
    
    #compute zdot
    zdot = velz
    
    #Compute all forces
    #gravity
    grav = -9.81*m
    
    #aerodynamic
    aero = 0.0
    
    #thrust
    thrust = 0.0
    
    F = grav + aero + thrust
    
    #compute zddot
    zddot =  F/m
    
    #compute statedot
    statedot = np.asarray([zdot,zddot])
    
    return statedot

##initial conditions
z0 = 0.0  ##m
velz0 = 164  ##m/s
state_initial = np.asarray([z0, velz0])


#time window
t_out = np.linspace(0,33.5,1000)
state_final = sci.odeint(Derivatives,state_initial, t_out)


###outputs
zout = state_final[:,0]
velzout = state_final[:,1]

##maximum altitude
max_alt = np.max(zout)
print("Maximum Altitude reached = ", max_alt,"m")

## max_alt = velz0^2 sin^2 theta/2g
## => velz0 sin theta = sqrt(2g*max_alt)
## at max_alt velz0 sin theta - gt = 0 
## => t = velz0 sin theta/g
## => t = sqrt(2g*max_alt)/g = sqrt(2*max_alt/g)


#total time of flight
t_tot = 2*np.sqrt(2*max_alt/9.81)
print("Total Time of Flight = ",t_tot, "secs")


##plotting
#Altitude plot
plt.figure()
plt.plot(t_out,zout, label = 'trajectory')
plt.xlabel('Time (s) -->')
plt.ylabel('Altitude (m) -->')
plt.grid()
plt.legend()

#Velocity Plot
plt.figure()
plt.plot(t_out,velzout, label = 'velocity')
plt.xlabel('Time (s) -->')
plt.ylabel('Velocity (m/s) -->')
plt.grid()
plt.legend()














