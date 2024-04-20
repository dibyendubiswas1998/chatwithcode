import os
from pathlib import Path
import logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s]: %(message)s")



# Project Structure:
project_name = "chatwithcode"
template_name = "chatwithcode"
list_of_files = [
    ".github/workflows/.gitkeep", # CICD pipeline files.
   
    "notebook/.gitkeep", # all the notebook related files.
    "documentation/.gitkeep", # all the documentation related to these project.
    "documentation/word_files/.gitkeep", # all the word files.
    "logs/logs.log", # store logs into local directory.

    f"src/{template_name}/__init__.py", # mongodb package.

    f"src/{template_name}/utils/__init__.py", # utils package.
    f"src/{template_name}/utils/common_utils.py", # common_utils module.
    f"src/{template_name}/utils/logging.py", # logging module.

    f"src/{template_name}/config/__init__.py", # config package.
    f"src/{template_name}/config/configuration.py", # configuration module.

    f"src/{template_name}/entity/__init__.py", # entity package.
    f"src/{template_name}/entity/config_entity.py", # config-entity module.

    f"src/{template_name}/constants/__init__.py", # constants package.
    
    f"src/{template_name}/components/__init__.py", # component package.
   
    f"src/{template_name}/pipeline/__init__.py", # create a pipeline package for this project.

    "artifacts/.gitkeep", # artifats directory
    "artifacts/data/.gitkeep", # store all the data here.


    "config/config.yaml", # config/config.yaml file.
    "config/secrect.yaml", # config/secrect.yaml file.
    ".env", # enviroments variables

    "templates/.gitkeep", # template directory for html file.
    "static/css/.gitkeep", # static/css directory for css file.
    "static/js/.gitkeep", # static/js directory for javascripts file.
    "static/image/.gitkeep", # static/image directory for images.

    "main.py", # main.py file.
    "setup.py", # setup.py file.
    "app.py", # app.py file.
    "requirements.txt", # requirements.txt file.

    "Dockerfile", # Dockerfile
]


def create_project_template(project_template_lst):
    """
        Creates directories and files based on the provided file paths.

        Args:
            project_template_lst (list): A list of file paths.

        Returns:
            None

        Raises:
            OSError: If there is an error creating directories or files.
            IOError: If there is an error creating directories or files.
            Exception: If there is an unknown error.

        Example Usage:
            project_template_lst = ['dir1/file1.txt', 'dir2/file2.txt', 'file3.txt']
            create_project_template(project_template_lst)
    """
    try:
        for filepath in project_template_lst:
            filepath = Path(filepath)
            file_dir, file_name = filepath.parent, filepath.name

            if file_dir != "":
                Path(file_dir).mkdir(parents=True, exist_ok=True)
                logging.info(f"Created directory: {file_dir}")

            if (not filepath.exists()) or (filepath.stat().st_size == 0):
                filepath.touch()
                logging.info(f"Created file: {filepath}")
            else:
                logging.info(f"{file_name} already exists")

    except (OSError, IOError) as e:
        logging.error(f"Error: {e}")
    except Exception as e:
        logging.error(f"Unknown error: {e}")
        



if __name__ == "__main__":
    logging.info(f"Created project template for: {project_name}")
    create_project_template(list_of_files)
