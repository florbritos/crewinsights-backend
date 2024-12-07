from api.services.pinecone_service import PineconeService
from api.services.langchain_service import LangchainService
from bson import ObjectId

class ReportService:
    def __init__(self):
        self.pinecone_service = PineconeService()
        self.langchain_service = LangchainService()

    def save(self, report):
        report_text = self.langchain_service.generateReportAsText(report)
        id_report = str(ObjectId())
        return self.pinecone_service.save(id_report, report_text.content)