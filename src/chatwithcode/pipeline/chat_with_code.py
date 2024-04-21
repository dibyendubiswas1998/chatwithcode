from chatwithcode.utils.common_utils import log, create_dir, clean_prev_dirs_if_exis
from chatwithcode.config.configuration import ConfigManager
from chatwithcode.components.data_ingestion import DataIngestion
from chatwithcode.components.vectordb_embeddings import StoreEmbeddings
from chatwithcode.components.generate_answer import GenerateResponse
import os



class ChatWithCode:
    def __init__(self) -> None:
        self.log_file = "logs/logs.log"
        self.config_manager = ConfigManager()
    
    def process(self, url:str) -> str:
        """
            Process the data from a GitHub repository, create a knowledge base, and store the embeddings.

            Args:
                url (str): The URL of the GitHub repository to be ingested.

            Raises:
                Exception: If an error occurs during the process.

            Example Usage:
                chat = ChatWithCode()  # Initialize the ChatWithCode object
                url = "https://github.com/example/repository"  # Specify the GitHub repository URL
                chat.process(url)  # Process the data from the GitHub repository
        """
        try:
            # Step 1: DataIngestion (cloning a GitHub repository into the directory, and logging the process)
            self.github_url_ingestion_confg = self.config_manager.get_github_url_ingestion_confg() # get the github configuration
            os.system(f'rd /s /q "{self.github_url_ingestion_confg.github_dir}"') # forcefully delete the existing github repository

            self.ingestion = DataIngestion(config=self.github_url_ingestion_confg) # initialize the DataIngestion class
            self.ingestion.get_data(url=url)


            # Step 2: Create KnowledgeBase:
            self.store_embedding_vectordb_config = self.config_manager.get_store_embedding_vectordb_config() # get the embedding configuration
            self.emb = StoreEmbeddings(config=self.store_embedding_vectordb_config) # initialize the class
            self.documents = self.emb.get_documents() # load data from given github directory
            self.chunks = self.emb.create_chunks(documents=self.documents) # create chunks of documents
            self.emb.create_knowledgebase(chunks=self.chunks) # create knowledgebase (store embedding to chromadb)

            return "Successfully !!!"

        except Exception as ex:
            log(file_object=self.log_file, log_message=f"Error occurred: {ex}")
            raise ex


    def predict(self, question:str):
        """
            Generates a response to a given question.

            Args:
                question (str): The question for which the answer is to be generated.

            Returns:
                str: The generated answer to the given question.

            Raises:
                Exception: If an error occurs during the prediction process.
        """
        try:
            self.store_embedding_vectordb_config = self.config_manager.get_store_embedding_vectordb_config() # get the embedding configuration
            self.emb = StoreEmbeddings(config=self.store_embedding_vectordb_config) # initialize the class

            # Step 1: Get the QA Chain
            self.llm_config = self.config_manager.get_llm_config() # get the llm configuration
            self.response = GenerateResponse(config=self.llm_config) # initialize the class
            self.qa_chain = self.response.qa_llm(retriever=self.emb.retriever(k=15)) # get the chain for generate the answers

            # Step 2: Generate the Answer based on question:
            self.result = self.response.generate_response(qa_chain=self.qa_chain, question=question) # get the relevant result from the cgiven context

            # Step 3: Return the answer
            return self.result

        except Exception as ex:
            log(file_object=self.log_file, log_message=f"Error occurred: {ex}")
            raise ex
        


if __name__ == "__main__":
    pp = ChatWithCode()
    pp.process(url="https://github.com/dibyendubiswas1998/Document-Tagging.git")
    # pp.predict(question="What is Data Ingestion?")