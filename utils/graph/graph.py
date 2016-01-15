# -*- coding: utf-8 -*-

import sys
import json

import matplotlib.pyplot as plt
import networkx as nx


def gen_graph(file_name):
    '''mode: show显示, save保存'''

    G = nx.Graph()

    for line in open(file_name):
        j = json.loads(line)
        url = j['url']
        links = j['links']

        G.add_node(url)
        G.node[url]['name'] = url

        for link in links:
            G.add_edge(url, link)

    return G


def draw_graph_matplotlib(G):
    pos = nx.spring_layout(G)

    plt.figure(1, figsize=(20, 20))
    node_labels = nx.get_node_attributes(G, 'name')

    nx.draw_networkx_labels(G, pos, labels=node_labels)

    nx.draw(G, pos, node_color='#A0CBE2', edge_color='#BB0000', width=5,
            edge_cmap=plt.cm.Blues, with_labels=True, labels=node_labels)

    plt.savefig("graph.png", dpi=1000, facecolor='w', edgecolor='w',
                orientation='portrait', papertype=None, format=None,
                transparent=False, bbox_inches=None, pad_inches=0.1)
    plt.show()


def draw_graph_graphml(G):
    pos = nx.spring_layout(G)

    node_labels = nx.get_node_attributes(G, 'name')
    nx.draw(G, pos, labels=node_labels, node_size=10)

    nx.write_graphml(G, 'graph.graphml')


if __name__ == '__main__':

    # generate graph
    G = gen_graph(sys.argv[1])

    # draw graph in matplotlib
    draw_graph_matplotlib(G)

    # save graph as graphml
    draw_graph_graphml(G)
