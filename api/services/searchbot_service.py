from api.services.metric_service import MetricService
from bson import ObjectId

class SearchBotService:
    def __init__(self):
        self.graph_service = MetricService()

    def search(self, query):
        id_metric = ObjectId()
        return self.graph_service.process_metric(id_metric, query)