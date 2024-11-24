from api.services.mongodb_service import MongoDB
from api.services.metric_service import MetricService
import numpy as np
import concurrent.futures
import json
from bson import ObjectId

class DashboardService:
    def __init__(self):
        self.mongodb_service = MongoDB()
        self.metric_service = MetricService()

    def getAllMetricsByUserId(self, id_user):
        response = self.mongodb_service.getOneDocument("Dashboard", {"_id": id_user})
        if response:
            metric_instructions = [self.mongodb_service.getOneDocument("Metrics", {"_id": metric}) for metric in response['metrics']]
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.metric_service.process_metric, metric['_id'], metric['metric']) for metric in metric_instructions]
            return [future.result() for future in concurrent.futures.as_completed(futures)]
        
    def delete(self, id_user, id_metric):
        self.mongodb_service.updateOne('Dashboard', {"id_user": id_user},{"$pull": {"metrics": ObjectId(id_metric)}})
        self.mongodb_service.deleteOne('Metrics', {"_id": id_metric})

    def add(self, id_user, id_metric, metric):
        self.mongodb_service.insertOne('Metrics', {
            "_id": id_metric,
            "metric": metric
        })
        self.mongodb_service.updateOne('Dashboard', {"id_user": id_user},{"$push": {"metrics": ObjectId(id_metric)}})