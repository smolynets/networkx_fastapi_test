from typing import Any

from sqlalchemy import select
from sqlalchemy.orm.session import Session

from models import Graph


def create_graph_query(session: Session, node_data: dict):
    """
    Create new Graph object.
    """
    db_graph = Graph(node_data=node_data)
    session.add(db_graph)
    session.commit()
    return db_graph


def get_graph_query(session: Session, graph_id: int):
    """
    Create new Graph object.
    """
    # graph_record = session.exec(select(Graph).where(Graph.id == graph_id)).first()
    graph_record = session.query(Graph).filter(Graph.id == graph_id).first()
    return graph_record


def update_graph_query(session: Session, graph_record_id: int, graph_data: dict):
    """
    Update Graph object.
    """
    # db_graph = session.exec(select(Graph).where(Graph.id == graph_record_id)).first()
    db_graph = session.query(Graph).filter(Graph.id == graph_record_id).first()
    db_graph.node_data = graph_data
    session.add(db_graph)
    session.commit()
    return db_graph