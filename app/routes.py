import networkx as nx
from app.dependencies import GraphManager
import json
from app.crud import create_graph_query, get_graph_query, update_graph_query
from app.models import Graph
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from app.database import get_db
from sqlalchemy.orm.session import Session
from app.schema import Edge, Node


router = APIRouter()

graph_manager = GraphManager()

@router.post("/graphs/")
def create_graph(session:Session=Depends(get_db)):
    """
    Create new Graph object.
    """
    graph_data = nx.readwrite.json_graph.node_link_data(graph_manager.graph)
    node_data = json.dumps(graph_data)
    db_graph = create_graph_query(session, node_data)
    return {"id": db_graph.id, "message": "Graph created"}


@router.post("/graphs/{graph_id}/add_node/{node_type}")
def add_node(graph_id: int, node_type: str, node_id: str, session:Session=Depends(get_db)):
    graph_record = get_graph_query(session, graph_id)
    if not graph_record:
        raise HTTPException(status_code=404, detail="Graph not found")
    graph = graph_manager.deserialize_graph(graph_record.node_data)
    graph_manager.add_start_node(graph, node_type, node_id)
    graph_data = graph_manager.serialize_graph(graph)
    update_graph_query(session, graph_record.id, graph_data)
    return {"message": graph_data}


@router.get("/nodes/start/{graph_id}")
def show_all_nodes(graph_id: int, session:Session=Depends(get_db)):
    graph_record = get_graph_query(session, graph_id)
    if not graph_record:
        raise HTTPException(status_code=404, detail="Graph not found")
    if graph_record.node_data:
        graph = graph_manager.deserialize_graph(graph_record.node_data)
        return graph_manager.show_all_nodes(graph)
    return {"message": "No nodes"}

@router.post("/edges/{graph_id}/add_edge/")
def create_edge(graph_id: int, edge: Edge, session:Session=Depends(get_db)):
    graph_record = get_graph_query(session, graph_id)
    if not graph_record:
        raise HTTPException(status_code=404, detail="Graph not found")
    graph = graph_manager.deserialize_graph(graph_record.node_data)
    graph.add_edge(edge.source, edge.target)
    graph_data = graph_manager.serialize_graph(graph)
    node = session.query(Graph).filter(Graph.id == graph_id).first()
    node.node_data = graph_data
    update_graph_query(session, graph_record.id, graph_data)
    return {"message": graph_data}


@router.get("/edges/start/{graph_id}")
def show_all_edges(graph_id: int, session:Session=Depends(get_db)):
    graph_record = get_graph_query(session, graph_id)
    if not graph_record:
        raise HTTPException(status_code=404, detail="Graph not found")

    graph = graph_manager.deserialize_graph(graph_record.node_data)
    return graph_manager.show_all_edges(graph)


@router.get("/path/{graph_id}")
def find_shortest_path(graph_id: int, start_node_id: str, end_node_id: str, session:Session=Depends(get_db)):
    graph_record = get_graph_query(session, graph_id)
    if not graph_record:
        raise HTTPException(status_code=404, detail="Graph not found")
    graph = graph_manager.deserialize_graph(graph_record.node_data)
    path = graph_manager.find_path(graph, start_node_id, end_node_id)
    return path