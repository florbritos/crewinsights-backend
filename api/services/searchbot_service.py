from api.services.mongodb_service import MongoDB
from api.services.langchain_service import LangchainService
from api.services.metric_service import MetricService
from api.services.image_service import ImageService
import numpy as np
from bson import ObjectId

class SearchBotService:
    def __init__(self):
        self.graph_service = MetricService()

    def search(self, query):
        id_metric = ObjectId()
        return self.graph_service.process_metric(id_metric, query)