import os
from chatwithcode.constants import *
from chatwithcode.entity.config_entity import *
from chatwithcode.utils.common_utils import read_params



class ConfigManager:
    def __init__(self, secrect_file_path=SECRET_FILE_PATH, config_file_path=CONFIG_FILE_PATH, 
                 params_file_path=PARAMS_FILE_PATH):
        
        self.secrect = read_params(secrect_file_path) # read information from config/secrect.yaml file
        self.config = read_params(config_file_path) # read information from config/config.yaml file
        self.params = read_params(params_file_path) # read information from config/params.yaml file
    

    def get_github_url_ingestion_confg(self) -> GithubUrlIngestionConfig:
        """
            Returns an instance of the GithubUrlIngestionConfig class with the github_dir attribute set to the value of self.config.artifacts.data.github_data.

            :return: An instance of the GithubUrlIngestionConfig class with the github_dir attribute set to the value of self.config.artifacts.data.github_data.
        """
        try:
            github_url_ingestion_confg = GithubUrlIngestionConfig(
                github_dir=self.config.artifacts.data.github_data
            )
            return github_url_ingestion_confg

        except Exception as ex:
            raise ex


    def get_store_embedding_vectordb_config(self) -> StoreEmbeddingVectorDBConfig:
        """
            Returns an instance of the `StoreEmbeddingVectorDBConfig` class with its attributes set based on the values obtained from the `params` and `config` files.

            :return: An instance of the `StoreEmbeddingVectorDBConfig` class with its attributes set based on the values obtained from the `params` and `config` files.
        """
        try:
            store_embedding_vectordb_config = StoreEmbeddingVectorDBConfig(
                chunk_zise=self.params.embeddings.chunk_zise,
                overlap=self.params.embeddings.overlap,
                embedding_model_name=self.config.model.embedding_model,
                github_dir=self.config.artifacts.data.github_data,
                chromadb_dir=self.config.artifacts.vectordb.chromadb_dir
            )
            return store_embedding_vectordb_config

        except Exception as ex:
            raise ex
    

    def get_llm_config(self) -> LLMConfig:
        try:
            self.llm = LLMConfig(
                llm=self.config.model.gemini_llm,
                temperature=self.params.gemini_llm.temperature,
                max_length=self.params.gemini_llm.max_length,
                json_file=self.config.artifacts.chatdata
            )

            return self.llm
        
        except Exception as ex:
            raise ex


        


if __name__ == '__main__':
    config_manager = ConfigManager()
    print(config_manager.get_llm_config())