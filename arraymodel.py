import matplotlib.pyplot as plt #for fancy graphs
import numpy as np #for fancy math
import random #for modelling random interactions

def arraymodel(infectiousness, survival_rate, vaccination, recovery_time):
  '''
  Models the spread of a disease with certain characteristics by creating an array of agents and randomizing contacts.
  '''
  size = 100 #size of 1 side of the array
  percentage_infected = 0.01 #percentage of population infected
  total_ticks = 60 #total ticks in the model - can represent days
  population_array = populate(vaccination, percentage_infected, recovery_time, size) #we populate the array
  t = np.linspace(0, total_ticks, total_ticks) #we want to record the progression of the different populations
  s = np.zeros(total_ticks)
  i = np.zeros(total_ticks)
  r = np.zeros(total_ticks)
  d = np.zeros(total_ticks)
 
  for j in range(total_ticks):
    population_array = increment(population_array, survival_rate) #decreases number of days that people are sick for and kills off people
    population_array = infect(population_array, infectiousness, recovery_time, size) #infects new people based on proximity
    s[j] = population_array.count(0)
    r[j] = population_array.count(-1) #-1 is the way I designate people as recovered, it's a kludge but it works for now
    d[j] = population_array.count(-2) #-2 is the way I designate people as dead
    i[j] = (size ** 2) - s[j] - r[j] - d[j]
 
  #plots our disease progression
  plt.plot(t,s,color='yellow',linewidth=2,label='Susceptible')
  plt.plot(t,i,color='red',linewidth=2,label='Infected')
  plt.plot(t,r,color='green',linewidth=2,label='Recovered')
  plt.plot(t,d,color='black',linewidth=2,label='Dead')
  plt.xlabel('time')
  plt.ylabel('number of people')
  plt.legend(loc='best')
  plt.show()
  
def populate(vaccination, percentage_infected, recovery_time, size): #populates the initial array
  population_array = []
  for i in range(size ** 2):
    if random.random() < percentage_infected: #make a person infected
      population_array.append(recovery_time)
    elif random.random() < vaccination: #make a person vaccinated(same as recovered)
      population_array.append(-1)
    else: #otherwise people are susceptible
      population_array.append(0)     
  return population_array
 
def increment(array, survival_rate): #decreases number of days that people are sick for and kills off people
  inc_array = []
  for i in range(len(array)):
    if array[i] > 1: #reduces number of days sick for
      inc_array.append(array[i] - 1)
    elif array[i] == 1: #decides whether someone recovers or dies
      if random.random() < survival_rate:
        inc_array.append(-1)
      else:
        inc_array.append(-2)
    else: #else just keep it how it is
      inc_array.append(array[i])
  return inc_array
 
def infect(array, infectiousness, recovery_time, size):
  infect_array = []
  for i in range(len(array)):
    if array[i] == 0:
      contacts = adjacent(i, array, size) #gets contacts from adjacent function
      infected_contacts = 0 #counts number of infected contacts
      for j in contacts:
        if j > 0:
          infected_contacts += 1
      #there is a certain chance to pass on the infection for every infected contact, increases with the number of infected contacts
      if random.random() > (1 - infectiousness) ** infected_contacts: 
        infect_array.append(recovery_time)
      else:
        infect_array.append(0)
    else:
      infect_array.append(array[i])
  return infect_array
 
#to change infection mechanics or to add different populations, all that needs to be done is change this function - it will not affect any other part of the simulation.
def adjacent(i, array, size):
  indexes = [i - size - 1, i - size, i - size + 1, #we take all the people adjacent to our person, this can be easily change
             i - 1, i + 1, 
             i + size - 1, i + size, i + size + 1]
  contacts = []
  for j in range(len(indexes)): #this loop just makes sure our indexes are correct, you can think of it like our array is on a torus
    if indexes[j] < 0:
      contacts.append(array[indexes[j] + size ** 2])
    elif indexes[j] >= size ** 2:
      contacts.append(array[indexes[j] - size ** 2])
    else:
      contacts.append(array[indexes[j]])
  return contacts
 
arraymodel(0.2,0.9,0.7,7)
