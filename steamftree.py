import requests
import ast
import random
import networkx as nx
import matplotlib.pyplot as plt

now = 76561199008790538
token = '220CB7667C6C55E2AF3D752FD5754942'
done = [now]
used = []
names = {}
tree = {}

for x in range(29):
    try:
        request = ast.literal_eval(requests.get(f'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key='
                                                f'{token}&steamid={now}&relationship=friend').text)
        tree[now] = []
        for y in request.get('friendslist').get('friends'):
            tree[now].append(y.get('steamid'))
        c = random.randint(0, len(tree[now]))
        while request.get('friendslist').get('friends')[c].get('steamid') == '' or \
                ast.literal_eval(requests.get(f"http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key={token}"
                                              f"&steamid={request.get('friendslist').get('friends')[c].get('steamid')}&"
                                              "relationship=friend").text) == {} or \
                request.get('friendslist').get('friends')[c].get('steamid') in done:
            c += 1
        now = request.get('friendslist').get('friends')[c].get('steamid')
        done.append(now)
    except IndexError:
        now = done[-2]

for x in tree.keys():
    c_names = []
    for y in ast.literal_eval(requests.get(
            f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={token}&steamids={tree.get(x)}').
                                      text).get('response').get('players'):
        c_names.append(y.get('personaname'))
    m_name = ast.literal_eval(requests.get(
        f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={token}&steamids={x}').text).get(
        'response').get('players')[0].get('personaname')
    names[m_name] = []
    for y in c_names:
        names[m_name].append(y)

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
plt.show()
