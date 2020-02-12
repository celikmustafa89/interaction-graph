from typing import Any

import networkx as nx

from bokeh.io import show, output_file
from bokeh.models import Plot, Range1d, MultiLine, Circle, HoverTool, BoxZoomTool, ResetTool
from bokeh.models.graphs import from_networkx
import psycopg2
import numpy as np


class DBClass(object):
    def __init__(self, router_name,device_id, os, connected_at, disconnected_at, kbps):
        self.device_id = device_id
        self.os = os
        self.router_name = router_name
        self.connected_at = connected_at
        self.disconnected_at = disconnected_at
        self.kbps = kbps


db = DBClass

from bokeh.palettes import *


try:
    #conn = psycopg2.connect("dbname= 'postgres' user= 'postgres' password ='test123'")
    conn = psycopg2.connect("dbname= 'ata_db' user= 'postgres' password =''")
    print ("connected")
except:
    print ("I am unable to connect to the database")


cur = conn.cursor()
cur.execute("SELECT device_id,router_name, os, connected_at, disconnected_at,kbps  from dataset1002 where device_id = 1001 or device_id = 1004 ")

#cur.execute("UPDATE dataset3 SET router_name = 'D2' where router_name ~* 'D2'")
conn.commit()
cols1=[];
cols= cur.fetchall()

count =0

for col in cols:
    x=DBClass(col[0],col[1],col[2],col[3],col[4],col[5])
    cols1.append(x)

    #cols[count] = col[0];
    #count+=1
def calculate():
    count =0
    for col in cols:
        count+=1
        print(col[0],col[1])
    print(count)

calculate()

router_names = []
def getRouterName():
    cur.execute("SELECT distinct router_name from dataset1002")
    routs = cur.fetchall()
    for col in routs:
        router_names.append(col[0]);
getRouterName()
router_set = set(router_names)



def karate_club_graph():
    """Return Zachary's Karate Club graph.

    Each node in the returned graph has a node attribute 'club' that
    indicates the name of the club to which the member represented by that node
    belongs, either 'Mr. Hi' or 'Officer'.

    Examples
    --------
    To get the name of the club to which a node belongs::

        >>> import networkx as nx
        >>> G = nx.karate_club_graph()
        >>> G.nodes[5]['club']
        'Mr. Hi'
        >>> G.nodes[9]['club']
        'Officer'

    References
    ----------
    .. [1] Zachary, Wayne W.
       "An Information Flow Model for Conflict and Fission in Small Groups."
       *Journal of Anthropological Research*, 33, 452--473, (1977).

    .. [2] Data file from:
       http://vlado.fmf.uni-lj.si/pub/networks/data/Ucinet/UciData.htm
    """
    # Create the set of all members, and the members of each club.
    all_members = set(range(6))
    club1 =  set(router_names)
    #club2 = all_members - club1

    G = nx.Graph()
    #G.add_nodes_from(all_members)
    G.add_nodes_from(club1)
    G.name = "test"

    zacharydat = """\
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1


"""

    for row, line in enumerate(zacharydat.split('\n')):
        thisrow = [int(b) for b in line.split()]
        for col, entry in enumerate(thisrow):
            if entry == 1:
                G.add_edge(row, col)

    # Add the name of each member's club as a node attribute.
    # for v in G:
    #     G.nodes[v]['test'] = 'test' if v in club1 else 'Officer'
    return G


# Prepare Data
G = karate_club_graph()

FRIEND_COLOR, NOT_FRIEND_COLOR = "red", "black"
edge_attrs = {}

for start_node, end_node, _ in G.edges(data=True):
    edge_color = FRIEND_COLOR if G.nodes[start_node] == G.nodes[end_node]["test"] else NOT_FRIEND_COLOR
    edge_attrs[(start_node, end_node)] = edge_color

nx.set_edge_attributes(G, edge_attrs, "edge_color")

# Show with Bokeh
plot = Plot(plot_width=400, plot_height=400,
            x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
plot.title.text = "Graph Interaction Demonstration"

node_hover_tools=[]
for col in cols:
    node_hover_tool = HoverTool(tooltips=[('Name',col[0]),("index", "@index"), (col[0], "@club")])
    plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())
graph_renderer = from_networkx(G, nx.spring_layout, scale=1, center=(0, 0))
graph_renderer.node_renderer.glyph = Circle(size=15, fill_color=Spectral4[0])
graph_renderer.edge_renderer.glyph = MultiLine(line_color="edge_color", line_alpha=0.8, line_width=1)
plot.renderers.append(graph_renderer)



output_file("interactive_graphs.html")
show(plot)