from .pinecone_service import PineconeService
from langchain_community.document_loaders import DirectoryLoader


class ReportService:
    def __init__(self):
        self.service_pinecone = PineconeService()
        

    def save_report(self, report_dict):
        '''Save a flight report into the db'''
        self.service_pinecone.save(report_dict)
        return {"status": "success", "message": "Report saved"}
    
    # def load_pdf_reports(self):
    #     '''Loads pdfs documents saved in computer to feed ai model'''
    #     loader = DirectoryLoader('doc', glob="**/*.pdf")
    #     docs = loader.load()
    #     split_docs = self.text_splitter.split_documents(docs)
    #     #self.service_pinecone.from_documents(split_docs)
    #     return {"status": "success", "message": "Documents loaded"}