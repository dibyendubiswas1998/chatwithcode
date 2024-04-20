import os
from chatwithcode.constants import *
from chatwithcode.entity.config_entity import *
from chatwithcode.utils.common_utils import read_params



class ConfigManager:
    def __init__(self, secrect_file_path=SECRET_FILE_PATH, config_file_path=CONFIG_FILE_PATH):
        
        self.secrect = read_params(secrect_file_path) # read information from config/secrect.yaml file
        self.config = read_params(config_file_path) # read information from config/config.yaml file
    

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



if __name__ == '__main__':
    config_manager = ConfigManager()
    print(config_manager.get_github_url_ingestion_confg())