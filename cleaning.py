import sys
import os
import pandas as pd
from datetime import datetime, date, time
import networkx as nx
import itertools
import operator
import json
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams


months = {'January': 1,'February': 2,'March': 3,'April': 4, 'May': 5 , 'June' : 6, 'July':7, 'August':8, 'September': 9, 'October':10, 'November':11, 'December' : 12 }
#create a network
G = nx.Graph()

#this function get a string, like the type we have in the travel logfile and
#converts it to a python format
def get_date(string):
    parts = string.split()
    month = int(months[parts[0]])
    year = int(parts[2])
    day = int(parts[1][:-2])
    return datetime(year,month,day)

def between_quotes(string):
    value = string.find("'")
    if value == -1:
        return string
    value2 = string[value+1:].find("'")
    test = string[0:value+1]
    a = len(test)
    return string[value+1:value2+a]

def get_city(location_path):
    parts  = location_path.split(',')
    if len(parts) < 4:
        return None,None
    else:
        return between_quotes(parts[3]), between_quotes(parts[2])

#this is to keep track of blog post number
#to avoid duplicates.
post_number = set()

#read the header line
sys.stdin.readline()

#dictionary to keep track of all the users
users = {}

for line in sys.stdin.readlines():
    line = line.strip()
    print line

    path = line[2:line.find(']')] #get the location section of each line
    rest = line[line.find(']')+3:] #get the remaining information

    rem = rest.split(',') #parse the remaining section

    blog_number = rem[1]
    
    #duplicate record
    if blog_number in post_number:
        continue #this is a duplicate, continue to the next line
    
    post_number.add(blog_number) #keep track of the different blog post numbers

    visit_date = get_date(rem[2]) #parse the date and convert it python form
    blogger_id = rem[3]  #get the unique blogger id


    #get city and state
    visit_city , visit_state = get_city(path)

    #if data doesnt have city or state, then discard
    if (visit_city == None) or (visit_state == None):
        continue

    #check if user info has been added, if not initialize
    if blogger_id not in users.keys():
        users[blogger_id] = []

    #add visit info, note, the same city can have multiple entries
    #because users can return to the same city, dates would be
    #different
    city_state_time = (visit_city,visit_state,visit_date)
    users[blogger_id].append(city_state_time)

    #add the node to the network
    # No edges are created here
    G.add_node(visit_city, state = visit_state)

print
print 'The total number of unique users is --> ' + str(len(users))
print



'''
f = open('blah', 'w')
for a in users.keys():
    f.write(a + '\n')
f.close()
'''
city_visit_freq = {}
no_places_visited_per_user = []

list_of_visited_city_set_for_each_user = []

#do histogram for city
#how travellers are going to a particular city
for user in users.keys():
    places = users[user]
    
    each_user_set = set()
    
    for place in places:
        each_user_set.add(place[0])
    
    list_of_visited_city_set_for_each_user.append(each_user_set)
    no_places_visited_per_user.append(len(each_user_set))

    for a in each_user_set:
        if a in city_visit_freq.keys():
            city_visit_freq[a] += 1
        else:
            city_visit_freq[a] = 1


#plt.hist(no_places_visited_per_user)

'''
d = sorted(city_visit_freq.iteritems(), key=operator.itemgetter(1))
values = []
labels = []
new_d = []
a = len(d)-1
for i in range(30):
    new_d.append(d[a])
    a = a-1
for a in new_d:
    values.append(a[1])
    labels.append(a[0])
rcParams['figure.figsize'] = (18,6)
ax = plt.gca()
ax.tick_params(axis='x', colors = 'blue')
ax.tick_params(axis='y', colors = 'red')
s = pd.Series(values, index = labels)
pd.Series.plot(s, kind='bar')
plt.show()
'''

for a in list_of_visited_city_set_for_each_user:
    
    lcity = list(a)
    edges_to_add = list(itertools.combinations(lcity,2))

    for u in edges_to_add:
               
        #check if the edges exists already and increment weight
        if u[1] in G.neighbors(u[0]):
            G[u[0]][u[1]]['weight'] = G[u[0]][u[1]]['weight'] + 1
            G[u[0]][u[1]]['difference'] = 1.0/float(G[u[0]][u[1]]['weight'])
        else:
            G.add_edge(u[0], u[1], weight = 1.0, difference = 1.0)

print 'before numpy'

np.random.seed(1)

pos = nx.spring_layout(G, k = 2, iterations = 20)

nx.draw_networkx_edges(G, pos, alpha = 0.05)

nx.draw_networkx_nodes(G, pos)

lbls = nx.draw_networkx_labels(G, pos, alpha=0.5, font_size = 6)

print 'before numpy 2'

plt.xticks([])
plt.yticks([])
plt.show()

