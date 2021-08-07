import pandas as pd
from math import sqrt
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def euclid_dist(q,p): #euclidean distance function that works for N dimensions
  e_dist = 0
  for i in range(3,len(q)):
    e_dist+=((q[i]-p[i])**2)
  e_dist = sqrt(e_dist)
  return e_dist

    
class KMeans:
  def __init__(self,toler=0.002,k=3,max_iterations=100):
    self.toler = toler #the model stops converging when the change reaches this tolerance
    self.k = k #number of clusters
    self.max_iterations = max_iterations #max iterations used for training the model to fit clusters to data
  
  def train(self,data):
    self.centroids = {} #position of K centroids
    self.classes = {} #data points that make up cluster
    for i in range(self.k):
      self.centroids[i]=data[i] #place centroids on first K data points

    for i in range(self.max_iterations): # for every iteration

      for ii in range(self.k): # for every cluster initialize a list 
        self.classes[ii]=[] 

      for point in data: # for every datapoint in the data
        distances = [] #list that holds distance, index of cluster
        for ii in range(self.k): #for every cluster
            # find dist between datapoint "point" and cluster centroid 'ii'
            distances.append([euclid_dist(point,self.centroids[ii]),ii]) 
        distances.sort() #sort all distances
        closest = distances[0][1] #the cluster that datapoint "point" is closest to
        self.classes[closest].append(point) #add datapoint "point" to that cluster

      old_centroids = dict(self.centroids) #save old centroids
    
      for ii in range(self.k): #for every centroid
        class_sum = np.zeros(len(data[0])) #empty array of zeros
        for j in self.classes[ii]: #for every point in cluster 'ii', add it to class_sum
          for k in range(3,len(j)):
            class_sum[k]+=j[k]
        self.centroids[ii]=class_sum/len(self.classes[ii]) #new centroid is avg of all new points in cluster

      converged = True

      for ii in range(self.k): #for all centroids...
        #if distance is above tolerance, it is not converged
        delta = abs(np.sum(((self.centroids[ii][3:]-old_centroids[ii][3:])/old_centroids[ii][3:])*100.0))
        #print(delta)
        if(delta>self.toler):
          converged = False
          break
      #print(converged)
      if converged == True:
        break

  def predict(self,point): #make it weighted sum depending on # watchers
    distances = [] #list of distances from 'point' to cluster 'i'
    for i in range(self.k):
      distances.append([euclid_dist(point,self.centroids[i]),i]) 
    distances.sort() #sort distances and return index of closest cluster
    return distances[0][1]
  
  def get_price(self,index):
    tot_watchers =0
    for i in self.classes[index]:
      tot_watchers+=i[1]
    price =0
    for i in self.classes[index]:
      price+= i[0]*(i[1]/tot_watchers)
    return price


  def get_links(self,point,index,k=3):
    sim = []
    for i in self.classes[index]:
      sim.append([euclid_dist(point,i),-i[1],i[2]])
    sim.sort()
    links = []
    for i in range(k):
      links.append(sim[i][2])
    return links

  def show_cluster(self,index): 
      mean=0
      for i in self.classes[index]:
          print(i)
          mean+=i[0]
      mean/=len(self.classes[index])
      print(mean)
  
  def accuracy(self,point,index):
    mean = 0
    for i in self.classes[index]:
          mean+=euclid_dist(point,i)
    mean/=len(self.classes[index])
    return mean
      
def optimize_model(k,dlist):
  k_means_clf = KMeans(k=k)
  k_means_clf.train(dlist)
  point =[0,0,0,2,20,0,1,14,64]
  index = k_means_clf.predict(point)
  return k_means_clf.accuracy(point=point,index=index)

def prepare_data():
  file =  open("output.csv")
  data = pd.read_csv(file)
  data = data[data['sale type']==1]
  data = data[data['views per hour']!=-1]
  data = data[data['price']!=-1]
  data = data.drop(columns=['color'])
  dlist = data.values.tolist()
  return dlist
