#defining a class for all the cities, this is probably overkill
class City:
  def __init__(self, name, x, y): #stores the name and coordinates of a city
    self.name = name
    self.x = x
    self.y = y
 
#here's the list of our cities
Cities = [City("Victoria", 48.4284, 123.3656),
          City("Whitehorse", 60.7212, 135.0568),
          City("Edmonton", 53.5461, 113.4938),
          City("Yellowknife", 53.5461, 113.4938),
          City("Regina", 50.4452, 104.6189),
          City("Winnipeg", 49.8951, 97.1384),
          City("Toronto", 43.6532, 79.3832),
          City("Iqaluit", 63.7467, 68.5170),
          City("Quebec City", 46.8139, 71.2080),
          City("Fredericton", 45.9636, 66.6431),
          City("Charlottetown", 46.2382, 63.1311),
          City("Halifax", 44.6488, 63.5752),
          City("St. John's", 47.5615, 52.7126)]
 
#we want to start from Ottawa, so we save it separately
Ottawa = City("Ottawa", 45.4215, 75.6972)
 
#Canada is big[citation needed] so we can't assume it's flat, so let's calculate distance on a sphere instead
def distance(A, B):
  x1 = A.x * (np.pi/180) #we convert to radians because degrees suck
  x2 = B.x * (np.pi/180)
  delta_x = abs(A.x - B.x) * (np.pi/180) #delta_x is just |x1 - x2|
  delta_y = abs(A.y - B.y) * (np.pi/180)
  #basically implement the haversine formula: https://en.wikipedia.org/wiki/Haversine_formula
  R = 6371 #radius of earth in km
  a = (np.sin(delta_x/2) ** 2) + (np.cos(x1) * np.cos(x2)) * (np.sin(delta_y/2) ** 2)
  c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
  return c * R
 
#We calculate route lengths a lot, so it's nice to have a separate function for it
def route_length(Start, Iternary):
  current_distance = distance(Start, Iternary[0]) + distance(Iternary[-1], Start)
  for i in range(len(Iternary) - 1): #w
    current_distance += distance(Iternary[i], Iternary[i+1])
  return current_distance
 
#We also plot routes a lot, so more self-contained code
def plot_route(Start, Iternary):
  Full_Iternary = [Start] + Iternary + [Start] #We add the starts to our iternary
  xs = [i.x for i in Full_Iternary] #extract x coordinates of iternary
  ys = [i.y for i in Full_Iternary] #extract y coordinates of iternary
  plt.plot(ys, xs, color='black', marker = 'o')
  plt.plot(Start.y, Start.x, color='red', marker = 'o') #plot start in a different color
  plt.gca().invert_xaxis() #we invert the axis because maps work that way for some reason
  plt.show()
 
#outputs all the info about a route
def output_route(Start, Iternary):
  plot_route(Start, Iternary) #plot our route
  cities_string = "The best route found was: " #we print this nice string with the cities we visit in order
  for A in Iternary: #we use this loop to complete cities_string
    cities_string += A.name 
    cities_string += ", "
  cities_string += Start.name
  print(cities_string)
  print("Total distance:", route_length(Start, Iternary), "km") #print distance

#greedy approach to calculating the best route
def greedy(Start, Iternary):
  Current_route = [Start] #our current route
  Cities_to_go = Iternary #cities we still need to visit
  while len(Cities_to_go) > 0: #while there are still cities we need to visit
    smallest_distance = distance(Current_route[-1], Cities_to_go[0])
    best_guess = Cities_to_go[0]
    for A in Cities_to_go: #find the closest city that we still need to go to
      if distance(Current_route[-1], A) < smallest_distance:
        smallest_distance = distance(Current_route[-1], A)
        best_guess = A
    Current_route.append(best_guess) #add the closest city to our route
    Cities_to_go.remove(best_guess) #remove it from the cities we still need to visit
  output_route(Start, Current_route) #output our route

greedy(Ottawa, Cities)
