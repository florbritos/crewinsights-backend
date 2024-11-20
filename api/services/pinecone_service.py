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
        #ya estaba funcionando
        #self.index_name = "pinecone-crewinsights"
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        #nuevo
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index = pc.Index("pinecone-crewinsights")
        embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"), model = "text-embedding-3-small")
        self.vector_store = PineconeVectorStore(index=self.index, embedding=embeddings)

    # #ya estaba funcionando
    # def getVectorStore(self):
    #     embedding = OpenAIEmbeddings(
    #         model = "text-embedding-3-small"
    #     )
    #     return PineconeVectorStore(embedding=embedding, index_name=self.index_name)

    #nuevo
    def getVectorStore(self):
        return self.vector_store

    def save(self, id_report, data):
        texts = []
        metadatas = []

        for key, text in data.items():
            chunks = self.text_splitter.split_text(str(text))
            for i, chunk in enumerate(chunks):
                texts.append(chunk)
                metadatas.append({
                    "id_report": id_report, 
                    "chunk_index": i,
                    "key": key,
                    "value": text,
                    "text": chunk
                })

        self.getVectorStore().add_texts(texts=texts, metadatas=metadatas)