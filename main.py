import networkx as nx
from github import Github
from operator import itemgetter
import matplotlib.pyplot as plt

access_token = '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'
username = 'OneLoneCoder'
repo_name = 'synth'

client = Github(access_token, per_page=100)
user = client.get_user(username)
repo = user.get_repo(repo_name)

stargazers = [s for s in repo.get_stargazers()]

g = nx.DiGraph()
g.add_node(repo.name + '(repo)', type='repo', lang=repo.language, owner=user.login)

for sg in stargazers:
    g.add_node(sg.login + '(user)', type='user', location=sg.location or 'None', repos=sg.public_repos)
    g.add_edge(sg.login + '(user)', repo.name + '(repo)', label='gazes')

    # We want to also see how many people don't specify their location
    loc = sg.location or 'None'
    g.add_node(loc, type='location')
    g.add_edge(sg.login + '(user)', loc, label='lives_in')

    year = sg.created_at.strftime("%Y")
    g.add_node(year + '(year)', type='yearCreated')
    g.add_edge(sg.login + '(user)', year + '(year)', label='createdAt')

x = sorted([
    (n, g.in_degree(n))
    for n in g.nodes
    if g.nodes[n]['type'] == 'yearCreated'], key=itemgetter(1), reverse=True)[:10]
print(x)


nx.write_gexf(g, r'C:\Users\Benjamin Hofer\PycharmProjects\gitAufgabe2\Results\graph.gexf')
