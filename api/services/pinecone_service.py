import os
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

class PineconeService():
    def __init__(self):
        self.pinecone_api_key = os.getenv('PINECONE_API_KEY')
        self.index_name = "pinecone-crewinsights"
        self.embeddings = OpenAIEmbeddings(
            model = "text-embedding-3-small"
        )
        self.vectorstore = PineconeVectorStore(embedding=self.embeddings, index_name=self.index_name)
        self.text_splitter = RecursiveCharacterTextSplitter()

    def save(self, report_dict):
        ''' '''
        texts = []
        metadatas = []
        report_id = None

        for key, text in report_dict.items():
            if key == "id":
                report_id = text
            else: 
                chunks = self.text_splitter.split_text(text)
                for i, chunk in enumerate(chunks):
                    texts.append(chunk)
                    metadatas.append({"report_id": report_id, "chunk_index": i})

        self.vectorstore.add_texts(texts=texts, metadatas=metadatas)