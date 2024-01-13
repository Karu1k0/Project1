from flask import Flask, render_template, jsonify, request
import osmnx as ox
import networkx as nx

app = Flask(__name__)

# Đường dẫn đến file OSM đã tải về
osm_file_path = 'D:/map-3.osm'

# Đọc dữ liệu từ file OSM và tạo đồ thị
graph = ox.graph_from_xml(osm_file_path)

coordinates=[[21.0031004,105.8876791],
             [21.0064649,105.8829755]]
print(graph.nodes)
edges = []
for u, v, data in graph.edges(data=True):
    print(data)
    break

print(type(list(graph.nodes)[0]))
def calculate_shortest_path():
    #data = request.get_json()
    #start_coords = data.get('start_coords')
    #//end_coords = data.get('end_coords')
    nodes=[]
    for point in coordinates:
        node=ox.distance.nearest_nodes(graph,*point)
        nodes.append(node)
        print(type(node))
    # Lấy node gần nhất với tọa độ bắt đầu và kết thúc
    #start_node = ox.distance.nearest_nodes(graph, *start_coords)
    #end_node = ox.distance.nearest_nodes(graph, *end_coords)

    # Tính đường đi ngắn nhất bằng thuật toán Dijkstra
    shortest_path = nx.approximation.traveling_salesman_problem(graph, nodes=nodes, weight='length')
    print(shortest_path)
calculate_shortest_path()
