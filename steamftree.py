import requests
import ast
import random
import networkx as nx
import matplotlib.pyplot as plt

# Values
now = 00000000000000000 # Put here the first Steam profile you want to tree. (SteamID 64)  
token = '' # Put here your Steam token (go here for generate: https://steamcommunity.com/dev/apikey)
repeat = 15 # Repeat is the number of time the script will find a friend (more the number is higher, more it take times (the best is 15))
done = [now]
used = []
names = {}
tree = {}

for x in range(repeat):
    try:
        request = ast.literal_eval(requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key='
                                                f'{token}&steamid={now}&relationship=friend').text) # Get the current person
        tree[now] = []
        for y in request.get('friendslist').get('friends'): # Get the friend of the current person
            tree[now].append(y.get('steamid'))
        c = random.randint(0, len(tree[now])) # Get random person in the friend of the current person
        while request.get('friendslist').get('friends')[c].get('steamid') == '' or \
                ast.literal_eval(requests.get(f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={token}"
                                              f"&steamid={request.get('friendslist').get('friends')[c].get('steamid')}&"
                                              "relationship=friend").text) == {} or \
                request.get('friendslist').get('friends')[c].get('steamid') in done: # This is for check if the next person to try is good for the tree (I think)
            c += 1
        now = request.get('friendslist').get('friends')[c].get('steamid')
        done.append(now)
    except IndexError:
        now = done[-2]

# Finish the indexing
for x in tree.keys():
    c_names = []
    for y in ast.literal_eval(requests.get(
            f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={token}&steamids={tree.get(x)}').
                                      text).get('response').get('players'): # Getting more friends
        c_names.append(y.get('personaname'))
    
    m_name = ast.literal_eval(requests.get(
        f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={token}&steamids={x}').text).get(
        'response').get('players')[0].get('personaname') # Getting everyone names
    names[m_name] = []
    for y in c_names:
        names[m_name].append(y)

# Generate the tree with the stuff
network = nx.Graph()
for x in names.keys():
    if x not in used:
        network.add_node(x)
        used.append(x)
    for y in names.get(x):
        if y not in used:
            network.add_node(y)
            used.append(y)
        network.add_edge(x, y)

nx.draw(network, with_labels=True)
plt.draw()
plt.show() # Showing the result
