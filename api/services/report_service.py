from .pinecone_service import PineconeService
from langchain_community.document_loaders import DirectoryLoader
from bson import ObjectId


class ReportService:
    def __init__(self):
        self.service_pinecone = PineconeService()
        
    def save(self, report):
        new_report = self.convert_bools_to_strings(report)
        id_report = str(ObjectId())
        return self.service_pinecone.save(id_report, new_report)
    
    def convert_bools_to_strings(self, data):
        return {key: str(value) if isinstance(value, bool) else value for key, value in data.items()}

    
    # def load_pdf_reports(self):
    #     '''Loads pdfs documents saved in computer to feed ai model'''
    #     loader = DirectoryLoader('doc', glob="**/*.pdf")
    #     docs = loader.load()
    #     split_docs = self.text_splitter.split_documents(docs)
    #     #self.service_pinecone.from_documents(split_docs)
    #     return {"status": "success", "message": "Documents loaded"}