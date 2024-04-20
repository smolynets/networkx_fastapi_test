import networkx as nx
import json

class GraphManager:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, graph, node_type, node_id):
        if node_type in ["start_node", "condition", "end_node"]:
            graph.add_node(node_id, node_type=node_type)
            return True
        elif node_type == "message":
            graph.add_node(node_id, node_type='message', status=status, message=message)
            return True
        else:
            return False

    def add_edge(self, graph, source_node, target_node):
        if source_node and graph.nodes[source_node]["node_type"] == "start_node":
            return False, "Edge not saved - start_node can has end edge only"
        if target_node and graph.nodes[target_node]["node_type"] == "end_node":
            return False, "Edge not saved - target_node can has start edge only"
        if source_node and target_node:
            graph.add_edge(source_node, target_node)
            return True, "Source and target nodes saved"
        else:
            if source_node:
                graph.add_edge(source_node, source_node)
                return True, "Source node saved"
            if target_node:
                graph.add_edge(target_node, target_node)
                return True, "Target_node node saved"
        return False, "Edge not saved - need source or target node"

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