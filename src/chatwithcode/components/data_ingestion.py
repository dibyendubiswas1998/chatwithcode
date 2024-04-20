from chatwithcode.utils.common_utils import log, clean_prev_dirs_if_exis, create_dir
from chatwithcode.entity.config_entity import GithubUrlIngestionConfig
from git import Repo


class DataIngestion:
    """
        Class responsible for cleaning and recreating a directory, cloning a GitHub repository into the directory, and logging the process.
    """
    def __init__(self, config: GithubUrlIngestionConfig) -> None:
        """
            Initializes the DataIngestion class.

            Args:
                config (GithubUrlIngestionConfig): An instance of the GithubUrlIngestionConfig class.
        """
        self.config = config
        self.log_file = "logs/logs.log" # mention the log file path
    
    def get_data(self, url:str) -> None:
        """
            Clean and recreate a directory, clone a GitHub repository into the directory, and log the process.

            Args:
                url (str): The URL of the GitHub repository to be cloned.

            Raises:
                Exception: If an error occurs during the process.

            Returns:
                None
        """
        try:
            clean_prev_dirs_if_exis(dir_path=self.config.github_dir) # clean directory if exists
            log(file_object=self.log_file, log_message=f"Successfully removed the existing directory: {self.config.github_dir}") # log the message

            create_dir(dirs=[self.config.github_dir]) # recreate the directory
            log(file_object=self.log_file, log_message=f"Successfully recreated the directory: {self.config.github_dir}") # log the message

            # save the github directory into local:
            Repo.clone_from(url=url, to_path=self.config.github_dir) # save the github files & folders
            log(file_object=self.log_file, log_message=f"Successfully cloned the GitHub repo: {url}") # log the message

        except Exception as ex:
            log(file_object=self.log_file, log_message=f"Error occurred: {ex}")
            raise ex
        





if __name__ == "__main__":
    from chatwithcode.config.configuration import ConfigManager
    config_manager = ConfigManager()
    github_url_ingestion_confg = config_manager.get_github_url_ingestion_confg()

    ingestion = DataIngestion(config=github_url_ingestion_confg)
    ingestion.get_data(url="https://github.com/dibyendubiswas1998/chatwithcode")