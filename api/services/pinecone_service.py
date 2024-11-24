from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

class PineconeService():
    def __init__(self):
        load_dotenv()
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50)
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index = pc.Index("pinecone-crewinsights")
        self.embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"), model = "text-embedding-ada-002") #"text-embedding-3-small"
        self.vector_store = PineconeVectorStore(index=self.index, embedding=self.embeddings)
    
    def getVectorStore(self):
        return self.vector_store
    
    def save(self, id_report, report_text):
        texts = []
        metadatas = []

        chunks = self.text_splitter.split_text(report_text)
        for i, chunk in enumerate(chunks):
            texts.append(chunk)
            metadatas.append({
                "id_report": id_report,
                "chunk_index": i,
                "text": chunk
            })

        self.getVectorStore().add_texts(texts=texts, metadatas=metadatas)

    # def save(self, id_report, data):
    #     texts = []
    #     metadatas = []

    #     for key, text in data.items():
    #         chunks = self.text_splitter.split_text(str(text))
    #         for i, chunk in enumerate(chunks):
    #             texts.append(chunk)
    #             metadatas.append({
    #                 "id_report": id_report, 
    #                 "chunk_index": i,
    #                 "key": key,
    #                 "value": text,
    #                 "text": chunk
    #             })

    #     self.getVectorStore().add_texts(texts=texts, metadatas=metadatas)