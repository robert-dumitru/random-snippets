import matplotlib.pyplot as plt #for fancy graphs
import numpy as np #for fancy math
import random #for modelling random interactions

def sirmodel(b, k, m, v, time):
  '''
  Implementation of SIR model for disease spread
  '''
  Implementation of SIR model to 
  t0 = 0 #initial time 
  t_end = time #end time 
  h = 0.001 #step size 
  steps = int((t_end - t0)/h + 1) # number of steps
  t = np.linspace(t0, t_end, steps) # storing t values
  S = np.zeros(steps) # for storing S values
  I = np.zeros(steps) # for storing I values
  R = np.zeros(steps) # for storing R values(which includes vaccinated people)
  D = np.zeros(steps) #for storing D values
  # initial conditions:
  S[0] = 1000*(1-v)
  I[0] = 1
  R[0] = 1000*v #we start out with a certain number of people vaccinated
  D[0] = 0
  N = I[0] + S[0] + R[0] + D[0]
  for n in range(steps-1): # range(start, stop, step)
    S[n+1] = S[n] + h*(-b)*S[n]*I[n]/N
    I[n+1] = I[n] + h*(((b*S[n]*I[n])/N) - k*I[n])
    R[n+1] = R[n] + h*(k*(1-m)*I[n])
    D[n+1] = D[n] + h*(k*m*I[n])
  plt.plot(t,S,color='yellow',linewidth=2,label='Susceptible')
  plt.plot(t,I,color='red',linewidth=2,label='Infected')
  plt.plot(t,R,color='green',linewidth=2,label='Recovered')
  plt.plot(t,D,color='black',linewidth=2,label='Dead')
  plt.xlabel('t (days)')
  plt.ylabel('S,  I, R, D')
  plt.legend(loc='best')
  plt.show()

sirmodel(1.83, 0.5, 0.05, 0, 60)
sirmodel(1.83, 0.5, 0.05, 0.3, 60)
sirmodel(1.83, 0.5, 0.05, 0.6, 60)
sirmodel(1.83, 0.5, 0.05, 0.9, 60)
