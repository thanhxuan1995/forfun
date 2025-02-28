from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

import os


class RetrieverTool:
    embeddings = HuggingFaceEmbeddings()

    def __init__(self, data_folder, save_path):
        if not os.path.exists(save_path):
            loader = DirectoryLoader(
                data_folder,
                glob="**/*.java",
                show_progress=True,
                use_multithreading=True,
            )
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=200
            )
            splits = text_splitter.split_documents(docs)
            vectorstore = FAISS.from_documents(
                documents=splits, embedding=self.embeddings
            )
            vectorstore.save_local(save_path)
            self.retriever = vectorstore.as_retriever()
        else:
            vectorstore = FAISS.load_local(
                save_path, self.embeddings, allow_dangerous_deserialization=True
            )
            self.retriever = vectorstore.as_retriever()

    def retrieve(self, query):
        retrieved_docs = self.retriever.invoke(query)
        return retrieved_docs

    def create_tool(self):
        return self.retriever
