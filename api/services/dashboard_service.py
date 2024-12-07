from api.services.mongodb_service import MongoDB
from api.services.metric_service import MetricService
import concurrent.futures
from bson import ObjectId

class DashboardService:
    def __init__(self):
        self.mongodb_service = MongoDB()
        self.metric_service = MetricService()

    def createDashboard(self, id_user):
        self.mongodb_service.insertOne('Dashboard', {
            "_id": id_user,
            "id_user": id_user,
            "metrics": []
        })

    def getDashboardByUserId(self, id_user):
        response = self.mongodb_service.getOneDocument("Dashboard", {"_id": id_user})
        if response:
            metric_instructions = [self.metric_service.get(metric) for metric in response['metrics']]
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(self.metric_service.process_metric, metric['_id'], metric['metric']) for metric in metric_instructions]
            return [future.result() for future in concurrent.futures.as_completed(futures)]
        
    def deleteMetricFromDashboard(self, id_user, id_metric):
        self.mongodb_service.updateOne('Dashboard', {"id_user": id_user},{"$pull": {"metrics": ObjectId(id_metric)}})
        self.metric_service.delete(id_metric)

    def addMetricToDashboard(self, id_user, id_metric, metric):
        self.metric_service.add(id_metric, metric)
        self.mongodb_service.updateOne('Dashboard', {"id_user": id_user},{"$push": {"metrics": ObjectId(id_metric)}})

    def deleteDashboard(self, id_user):
        self.mongodb_service.deleteOne('Dashboard', {"_id": id_user})