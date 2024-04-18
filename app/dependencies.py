import networkx as nx
import json

class GraphManager:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_start_node(self, graph, node_type, node_id):
        graph.add_node(node_id, node_type=node_type)

    def add_message_node(self, node_id, status, message):
        self.graph.add_node(node_id, node_type='Message', status=status, message=message)

    def add_condition_node(self, node_id):
        self.graph.add_node(node_id, node_type='Condition')

    def add_end_node(self, node_id):
        self.graph.add_node(node_id, node_type='End')

    def add_edge(self, source_node, target_node):
        self.graph.add_edge(source_node, target_node)

    def remove_node(self, node_id):
        self.graph.remove_node(node_id)

    def remove_edge(self, source_node, target_node):
        self.graph.remove_edge(source_node, target_node)

    def show_all_nodes(self, graph=None):
        if graph:
            nodes = graph.nodes(data=True)
        else:
            nodes = self.graph.nodes(data=True)
        for node, attributes in nodes:
            print("Node ID:", node)
            print("Node Type:", attributes.get('node_type'))
            if attributes.get('node_type') == 'Message':
                print("Status:", attributes.get('status'))
                print("Message:", attributes.get('message'))
            return nodes

    def show_all_edges(self, graph=None):
        if graph:
            edges = graph.edges(data=True)
        else:
            edges = self.graph.edges(data=True)
        serialized_edges = []
        for edge in edges:
            serialized_edge = {
                "source": edge[0],
                "target": edge[1],
                "data": edge[2] if len(edge) > 2 else {}
            }
            serialized_edges.append(serialized_edge)
        return json.dumps(serialized_edges)

    def serialize_self_graph(self):
        return json.dumps(nx.node_link_data(self.graph))

    def serialize_graph(self, data):
        return json.dumps(nx.node_link_data(data))

    def deserialize_self_graph(self, data):
        self.graph = nx.node_link_graph(json.loads(data))


    def deserialize_graph(self, json_str):
        data = json.loads(json_str)
        graph = nx.node_link_graph(data)
        return graph

    def find_path(self, graph, start_id, end_id):
        try:
            return nx.shortest_path(graph, source=start_id, target=end_id)
        except nx.NetworkXNoPath:
            return None