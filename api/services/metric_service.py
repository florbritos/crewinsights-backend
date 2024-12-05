from api.services.graph_service import GraphService
from api.services.mongodb_service import MongoDB
import numpy as np
import json

class MetricService:
    def __init__(self):
        self.graph_service = GraphService()
        self.mongodb_service = MongoDB()

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
        
    def delete(self, id_metric):
        self.mongodb_service.deleteOne('Metrics', {"_id": id_metric})

    def get(self, id_metric):
        return self.mongodb_service.getOneDocument("Metrics", {"_id": id_metric})
    
    def add(self, id_metric, metric):
        self.mongodb_service.insertOne('Metrics', {
            "_id": id_metric,
            "metric": metric
        })