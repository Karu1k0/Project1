# __init__.py
from flask import Flask, render_template, jsonify, request
import osmnx as ox
import networkx as nx

app = Flask(__name__)

# Đường dẫn đến file OSM đã tải về
osm_file_path = 'D:/map-3.osm'

# Đọc dữ liệu từ file OSM và tạo đồ thị
graph = ox.graph_from_xml(osm_file_path)

@app.route('/')
def index():
    return render_template('index.html')  # Trả về trang index.html

@app.route('/get_map_data')
def get_map_data():
     # Convert đồ thị thành dạng dữ liệu có thể gửi đi (ví dụ: danh sách các cung)
    edges = []
    for u, v, data in graph.edges(data=True):
        edge = {
            'start': (graph.nodes[u]['y'], graph.nodes[u]['x']),
            'end': (graph.nodes[v]['y'], graph.nodes[v]['x']),
            'length': data.get('length', 0)
        }
        edges.append(edge)

    return jsonify({'edges': edges})

@app.route('/calculate_shortest_path', methods=['POST'])
def calculate_shortest_path():
    data = request.get_json()
    #start_coords = data.get('start_coords')
    #//end_coords = data.get('end_coords')
    coordinates=data.get('coordinates')
    nodes=[]
    for point in coordinates:
        node=ox.distance.nearest_nodes(graph,*point)
        nodes.append(node)
    # Lấy node gần nhất với tọa độ bắt đầu và kết thúc
    #start_node = ox.distance.nearest_nodes(graph, *start_coords)
    #end_node = ox.distance.nearest_nodes(graph, *end_coords)

    # Tính đường đi ngắn nhất bằng thuật toán Dijkstra
    shortest_path = nx.approximation.traveling_salesman_problem(graph, nodes, weight='length')

    print(shortest_path)
    # Convert đường đi thành dạng dữ liệu có thể gửi đi
    path_data = []
    for node in shortest_path:
        path_data.append({
            'lat': graph.nodes[node]['y'],
            'lon': graph.nodes[node]['x']
        })

    return jsonify({'path': path_data})

if __name__ == '__main__':
    app.run(debug=True)
