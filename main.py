import psycopg2
import networkx as nx
from bokeh.models import Plot, Range1d, HoverTool, BoxZoomTool, ResetTool, from_networkx, Circle, MultiLine
import datetime
import matplotlib.pyplot as plt


def retrieveDataFromDB():
    try:
        #conn = psycopg2.connect("dbname= 'postgres' user= 'postgres' password ='test123'")
        conn = psycopg2.connect("dbname='postgres' port='5433' user='postgres' password =''")
        print("connected")
    except:
        print("I am unable to connect to the database")

    cur = conn.cursor()
    #cur.execute("SELECT router_name, os, connected_at, disconnected_at  from dataset100 where device_id = 1001")
    cur.execute(
        "SELECT router_name, os, connected_at, disconnected_at  from dataset100v where device_id = 318849")
    #cur.execute("SELECT router_name, os, connected_at, disconnected_at  from dataset100 where device_id = 1055 order by connected_at")

    conn.commit()
    user1_records = cur.fetchall()

    #cur.execute("SELECT router_name, os, connected_at, disconnected_at  from dataset100 where device_id = 1004")
    cur.execute(
        "SELECT router_name, os, connected_at, disconnected_at  from dataset100v where device_id = 305894")
    #cur.execute("SELECT router_name, os, connected_at, disconnected_at  from dataset100 where device_id = 1067 order by connected_at")

    # conn.commit()
    user2_records = cur.fetchall()

    cur.execute("SELECT distinct router_name from dataset100v")
    routers = cur.fetchall()

    router_list = []
    for route in routers:
        router_list.append(route[0])

    print(user1_records)
    print(user2_records)
    print(routers)
    return user1_records, user2_records, router_list


user1_records, user2_records, distinct_routers = retrieveDataFromDB()

user1_routers = {}
user2_routers = {}

k1 = user1_records[0]
tt = k1[2]
timestring = user1_records[0][2].date().ctime()

# for router in distinct_routers:
#     user1_routers[router] = 0
#     user2_routers[router] = 0

for record in user1_records:
    time_spent = (record[3] - record[2]).total_seconds()/60.0 # burada harcanan zaman bulunur
    key=record[0]+ "-" +(record[2].date().ctime())
    if key in user1_routers.keys():
        user1_routers[key] = user1_routers[key] + time_spent
    else:
        user1_routers[key] = 0

for record in user2_records:
    time_spent = (record[3] - record[2]).total_seconds()/60.0 # burada harcanan zaman bulunur
    key = record[0] + "-" + (record[2].date().ctime())
    if key in user2_routers.keys():
        user2_routers[key] = user2_routers[key] + time_spent
    else:
        user2_routers[key] = 0



G = nx.Graph()
for router in distinct_routers:
    G.add_node(router)

common_nodes = [];
for k1, v1 in user1_routers.items():
    for k2, v2 in user2_routers.items():
        if k1 == k2 and v1 > 12 and v2 > 12:
            common_nodes.append(k1.split("-")[0])

common_nodes = list(set(common_nodes))
for node1 in common_nodes:
    for node2 in common_nodes:
        G.add_edge(node1, node2)


# router_colors = {}
# for router in distinct_routers:
#     if user1_routers.get(router) > 2 and user2_routers.get(router) > 2:
#         router_colors[router] = "red"
#     else:
#         router_colors[router] = "black"


# router_colors_temp = router_colors
# for k, v in router_colors.items():
#     for k1, v1 in router_colors.items():
#         if k1 is k:
#             continue
#         if v is "red" and v1 is "red":
#             G.add_edge(k, k1, color='red')
#         #else:
#             #G.add_edge(k, k1, color='black')

nx.draw_networkx(G, with_labels=True)
plt.show() # display
