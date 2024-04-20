from chatwithcode.utils.common_utils import log, insert_data_tojson_file
from chatwithcode.entity.config_entity import LLMConfig
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from datetime import datetime


# Load environment variables from .env file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


class GenerateResponse:
    """
        The GenerateResponse class is responsible for generating responses to questions using a language model (LLM) and a retrieval-based question answering (QA) chain. It loads the LLM, creates the QA chain, and generates a response based on the given question.
    """
    def __init__(self, config:LLMConfig) -> None:
        self.config = config
        self.log_file = "logs/logs.log"

    
    def load_llm(self):
        """
            Loads the language model (LLM) used for generating responses.

            Returns:
                ChatGoogleGenerativeAI: The loaded instance of the language model.

            Raises:
                Exception: If an error occurs while loading the LLM.
        """
        try:
            self.llm = ChatGoogleGenerativeAI(model=self.config.llm, google_api_key=GOOGLE_API_KEY, temperature=self.config.temperature, max_length=self.config.max_length) # load the llm
            log(file_object=self.log_file, log_message=f"load the llm, i.e. '{self.config.llm}'") # logs the message

            return self.llm

        except Exception as ex:
            log(file_object=self.log_file, log_message=f"Error occurred: {ex}") # log the exception
            raise ex
    

    def qa_llm(self, retriever):
        """
            Create a retrieval-based question answering (QA) chain using a language model (LLM).

            Args:
                retriever (object): The retriever object used for retrieving relevant documents for the QA chain.

            Returns:
                object: The created QA chain.

            Raises:
                Exception: If an error occurs during the creation of the QA chain.

            Example Usage:
                # Initialize the GenerateResponse class object
                response = GenerateResponse(config=llm_config)

                # Create a retriever object
                retriever = emb.retriever(k=17)

                # Create the QA chain
                qa_chain = response.qa_llm(retriever=retriever)

                # Invoke the QA chain with a question
                res = response.generate_response(qa_chain=qa_chain, question='Tell me something about the Project')

                # Print the response
                print(res)
        """
        try:
            # create qa_prompt template:
            qa_template = """
            Use the following information from the context (separated with <ctx></ctx>) to answer the question.
            If you don't know the answer, answer with "Unfortunately, I don't have the information." \
            If you don't find enough information below, also answer with "Unfortunately, I don't have enough information." \
            ------
            <ctx>
            {context}
            </ctx>
            ------
            <hs>
            {chat_history}
            </hs>
            ------
            {question}
            Helpful Answer:
            """
            qa_prompt = PromptTemplate(template=qa_template, input_variables=['context', 'chat_history', 'question']) # define Prompt template

            # create custom summary prompt:
            custom_summary_prompt='''Generate the overall summary of the following text (within the 512 words) that includes the following below elements:

            * A title that accurately reflects the content of the text.
            * An introduction paragraph that provides an overview of the topic.
            * Bullet points that list the key points of the text.
            * A conclusion paragraph that summarizes the main points of the text.

            Text:`{context}`'''
            custom_summary_template = PromptTemplate(template=custom_summary_prompt, input_variables=['context'])

            # define memory:
            memory = ConversationBufferWindowMemory(
                llm=self.load_llm(),
                memory_key="chat_history",
                input_key="question",
                k=3
            )

            chain_type_kwargs={
                "prompt": qa_prompt,
                "memory": memory
            }

            # create RetrievaQA chain:
            qa_chain = RetrievalQA.from_chain_type(llm=self.load_llm(),
                                                    chain_type="stuff",
                                                    retriever=retriever,
                                                    chain_type_kwargs=chain_type_kwargs
                                                )
        
            log(file_object=self.log_file, log_message=f"create qa prompt, custom summary prompt, define memory i.e. 'ConversationBufferWindowMemory, k=3', define RetrievalQA and return the qa_chain") # logs the message

            return qa_chain
    
        except Exception as ex:
            log(file_object=self.log_file, log_message=f"Error occurred: {ex}") # log the exception
            raise ex


    def generate_response(self, qa_chain, question:str):
        """
            Generates a response to a given question using a question answering (QA) chain.

            Args:
                qa_chain (QAChain): The QA chain object created using the `qa_llm` method.
                question (str): The question for which the response needs to be generated.

            Returns:
                str: The generated response to the given question.

            Raises:
                Exception: If an error occurs during the generation of the response.
        """
        try:
            self.ans = qa_chain.invoke(question) # get the response
            self.data_dct = {
                "date": str(datetime.now().date()), "time": str(datetime.now().strftime("%H:%M:%S")),
                "question": question,
                "answer": self.ans['result'].strip()
            }

            insert_data_tojson_file(file_path=self.config.json_file, data_dct=self.data_dct) # insert data to json file
            log(file_object=self.log_file, log_message=f"get the response based on result and store into '{self.config.json_file}'") # logs the message

            return self.ans['result'].strip()

        except Exception as ex:
            log(file_object=self.log_file, log_message=f"Error occurred: {ex}") # log the exception
            raise ex



if __name__ == "__main__":
    from chatwithcode.config.configuration import ConfigManager
    from chatwithcode.components.vectordb_embeddings import StoreEmbeddings
    config_manager = ConfigManager()
    
    llm_config = config_manager.get_llm_config()
    store_embedding_vectordb_config = config_manager.get_store_embedding_vectordb_config()
    emb = StoreEmbeddings(config=store_embedding_vectordb_config)

    response = GenerateResponse(config=llm_config)
    qa_chain = response.qa_llm(retriever=emb.retriever(k=17))
    res = response.generate_response(qa_chain=qa_chain, question="explain the code?")
    print(res)
