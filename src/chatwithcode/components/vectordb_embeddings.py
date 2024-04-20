from chatwithcode.utils.common_utils import log, clean_prev_dirs_if_exis, create_dir
from chatwithcode.entity.config_entity import StoreEmbeddingVectorDBConfig
from langchain.text_splitter import Language
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from typing import List
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")


class StoreEmbeddings:
    """
        The StoreEmbeddings class is responsible for loading an embedding model, loading and splitting documents, creating a knowledge base by
        storing embeddings of document chunks, and retrieving top results from the knowledge base.
    """
    def __init__(self, config: StoreEmbeddingVectorDBConfig) -> None:
        self.config = config
        self.log_file = "logs/logs.log"
    

    def load_embedding_model(self) -> HuggingFaceEmbeddings:
        """
            Load the embedding model using the specified model name from the configuration.

            Returns:
                HuggingFaceEmbeddings: The loaded embedding model.

            Raises:
                Exception: If an error occurs while loading the embedding model.
        """
        try:
            self.embeddings = HuggingFaceEmbeddings(model_name=self.config.embedding_model_name) # load the embedding model
            log(file_object=self.log_file, log_message=f"load the embedding model, i.e. '{self.config.embedding_model_name}'") # log the message

            return self.embeddings # return embeding model

        except Exception as ex:
            log(file_object=self.log_file, log_message=f"Error occurred: {ex}") # log the exception
            raise ex
    
    
    def get_documents(self) -> List[Document]:
        """
            Load and return the documents from the specified directory.

            Returns:
                documents (list): A list of loaded documents from the specified directory.

            Raises:
                Exception: If an error occurs during the loading process.
        """
        try:
            # load the data from github directory:
            self.loader = GenericLoader.from_filesystem(path=self.config.github_dir,
                                                        glob="**/*",
                                                        suffixes=[".py"],
                                                        parser=LanguageParser(language=Language.PYTHON, parser_threshold=500)
                                                        )
            self.documents = self.loader.load()  # load the data as document
            log(file_object=self.log_file, log_message=f"successfully load the documents from '{self.config.github_dir}', where size is '{len(self.documents)}'")  # logs the message

            return self.documents  # return the documents

        except Exception as ex:
            log(file_object=self.log_file, log_message=f"Error occurred: {ex}")  # log the exception
            raise ex


    def create_chunks(self, documents) -> List[Document]:
        """
            Splits the input documents into smaller chunks using the RecursiveCharacterTextSplitter class.

            Args:
                documents (list): A list of documents to be split into chunks.

            Returns:
                list: A list of smaller chunks obtained by splitting the input documents.
        """
        try:
            self.documents_splitter = RecursiveCharacterTextSplitter.from_language(
                language=Language.PYTHON,
                chunk_size=self.config.chunk_zise,
                chunk_overlap=self.config.overlap
            )
            self.chunks = self.documents_splitter.split_documents(documents)
            log(file_object=self.log_file, log_message=f"successfully perform the chunkings, where chunks  size is '{len(self.chunks)}'") # logs the message

            return self.chunks

        except Exception as ex:
            log(file_object=self.log_file, log_message=f"Error occurred: {ex}") # log the exception
            raise ex


    def create_knowledgebase(self, chunks) -> None:
        """
            Create a knowledge base by storing embeddings of chunks of documents into a Chroma database.

            Args:
                chunks (list): A list of smaller chunks obtained by splitting the input documents.

            Returns:
                None

            Raises:
                Exception: If an error occurs during the process.

            Example Usage:
                config = StoreEmbeddingVectorDBConfig()
                store_embeddings = StoreEmbeddings(config)
                chunks = store_embeddings.create_chunks(documents)
                store_embeddings.create_knowledgebase(chunks)
        """
        try:
            self.persist_directory = self.config.chromadb_dir # get the path of chromadb

            clean_prev_dirs_if_exis(dir_path=self.persist_directory) # clean the directory if already exists
            log(file_object=self.log_file, log_message=f"successfully clean the existing directory '{self.persist_directory}'") # logs the message

            create_dir(dirs=[self.persist_directory]) # recreate the directory
            log(file_object=self.log_file, log_message=f"successfully recreate directory '{self.persist_directory}'") # logs the message

            # store embeddings into vectordb:
            self.chroma_vector_db = Chroma.from_documents(documents=chunks,
                                                          embedding=self.load_embedding_model(),
                                                          persist_directory=self.persist_directory
                                                        )

            log(file_object=self.log_file, log_message=f"successfully store the embeddings into chromadb, path '{self.config.chromadb_dir}'") # logs the message


        except Exception as ex:
            log(file_object=self.log_file, log_message=f"Error occurred: {ex}") # log the exception
            raise ex


    def retriever(self, k:int) -> List[Document]:
        """
            Retrieves the top k results from a Chroma database using the specified embedding model.

            Args:
                k (int): The number of top results to retrieve.

            Returns:
                object: An object that contains the top k results from the Chroma database.

            Raises:
                Exception: If an error occurs during the retrieval process.
        """
        try:
            self.persist_directory = self.config.chromadb_dir # get the path of chromadb.
            log(file_object=self.log_file, log_message=f"get the chromadb path i.e. '{self.persist_directory}'") # logs the message

            self.vectordb = Chroma(persist_directory=self.persist_directory, embedding_function=self.load_embedding_model()) # get the vectordb

            self.retriever = self.vectordb.as_retriever(search_kwargs={"k": k}) # retrieve top k information
            log(file_object=self.log_file, log_message=f"retrieve the top k reseult from chromadb") # logs the message

            return self.retriever # return retriever

        except Exception as ex:
            log(file_object=self.log_file, log_message=f"Error occurred: {ex}") # log the exception
            raise ex





if __name__ == "__main__":
    from chatwithcode.config.configuration import ConfigManager
    config_manager = ConfigManager()
    store_embedding_vectordb_config = config_manager.get_store_embedding_vectordb_config()

    emb = StoreEmbeddings(config=store_embedding_vectordb_config)
    emb.load_embedding_model()
    documents = emb.get_documents()
    chunks = emb.create_chunks(documents=documents)
    emb.create_knowledgebase(chunks=chunks)
    retriever = emb.retriever(k=10)
    print(retriever.get_relevant_documents("what is DataIngestion?"))