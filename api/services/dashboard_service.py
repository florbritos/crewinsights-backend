from api.services.mongodb_service import MongoDB
from api.services.langchain_service import LangchainService
from api.services.graph_service import GraphService
from api.services.image_service import ImageService
import numpy as np
import concurrent.futures

class DashboardService:
    def __init__(self):
        self.mongodb_service = MongoDB()
        self.langchain_service = LangchainService()
        self.graph_service = GraphService(self.langchain_service)
        self.image_service = ImageService()

    def getAllMetricsByUserId(self, id_user):
        response = self.mongodb_service.getOneDocument("Dashboard", {"_id": id_user})
        if response:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.process_metric, metric, id_user) for metric in response['metrics']]
            return [future.result() for future in concurrent.futures.as_completed(futures)]

    def process_metric(self, metric, id_user):
        graph = self.graph_service.generate_graph(metric)
        if graph:
            graph_json = graph.to_dict()

            for key, values in graph_json.items():
                for i, value in enumerate(values):
                    if isinstance(value, dict):
                        if 'x' in value and isinstance(value['x'], np.ndarray):
                            value['x'] = value['x'].tolist()
                        
                        if 'y' in value and isinstance(value['y'], np.ndarray):
                            value['y'] = value['y'].tolist()

            base64_image = self.image_service.save_fig_to_image(graph)  
            insight = self.langchain_service.analyze_graph_image(base64_image)
            return {
                "graph_data": graph_json,
                "insight": insight
            }
        else:
            return {
                "graph_data": None,
                "insight": "No graph was generated."
            }