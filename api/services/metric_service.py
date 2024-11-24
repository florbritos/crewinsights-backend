from api.services.graph_service import GraphService
import numpy as np
import json

class MetricService:
    def __init__(self):
        self.graph_service = GraphService()

    def process_metric(self, id_metric, metric):
        analysis, graph = self.graph_service.generate_graph(metric)
        if graph:
            return {
                "graph_data": json.loads(graph.to_json()),
                "analysis": analysis,
                "id_metric": str(id_metric)
            }
        else:
            return {
                "graph_data": None,
                "analysis": analysis,
                "id_metric": str(id_metric)
            }