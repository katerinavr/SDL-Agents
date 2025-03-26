import os
from typing import Dict, Any
import PyPDF2
import autogen
from autogen import (
    UserProxyAgent,
    AssistantAgent,
    ConversableAgent,
    register_function,
)
from autogen.coding import LocalCommandLineCodeExecutor
# from autogen.agentchat.contrib.capabilities.teachability import Teachability
# import autogen_llm
from utils.teachability_filtered import DedupTeachability
from config.settings import OPENAI_API_KEY, anthropic_api_key
from utils.system_messages import code_writer_system_message

def get_llm_config(llm_type: str) -> Dict[str, Any]:
    """
    Get LLM configuration based on the selected model type.    
    Args:
        llm_type (str): Type of LLM to use ('gpt4', 'claude')        
    Returns:
        dict: LLM configuration dictionary
    """
    llm_configs = {
        'gpt4o-mini': {
            "model": "gpt-4o-mini",
            'api_key': OPENAI_API_KEY,
            'temperature':0,
            "cache_seed": 0,
        },
        'gpt4o': {
            "model": "gpt-4o",
            'api_key': OPENAI_API_KEY,
            'temperature':0,
            "cache_seed": 0,
        },
        'claude_35': {
            "model": "claude-3-5-sonnet-20240620",
            'api_key': anthropic_api_key,
            'api_type': 'anthropic',
            'temperature':0,
            "cache_seed": 0,
   
        },
        'ArgoLLMs': {  # Local client operates only within the organization
            "model": "gpto1preview",
            "model_client_cls": "ArgoModelClient",
            'temperature': 0,
            "cache_seed": 0,
        }
    }
    
    return llm_configs.get(llm_type, llm_configs['ArgoLLMs'])

def pdf_to_text(pdf_file: str) -> str:
    """
    Extract text from a PDF file.
    
    Args:
        pdf_file (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text


def save_code(code: str, filepath: str) -> str:
    """Save the generated code to a specified file location"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save the code to the file
    with open(filepath, 'w') as f:
        f.write(code)
    return f"Code saved successfully to {filepath}"


class TerminatingUserProxyAgent(UserProxyAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def is_termination_msg(self, msg):
        """Custom termination condition implementation"""
        if msg.get("content") is not None:
            content = msg.get("content")
            if "TERMINATE" in content:
                return True
            
            # Check for successful code execution message
            if ">>>>>>>> EXECUTING CODE BLOCK" in content:

                if "exitcode: 0" in content or "execution succeeded" in content:
                    return True
                
                if "execution failed" in content :
                    return False
                return True
                
            # Check for the "Next speaker" message that indicates the conversation is stuck
            if "Next speaker:" in content and "admin" in content:
                return True
                
        return False

class AutoGenSystem:
    def __init__(self, llm_type: str, workdir: str, polybot_file_path: str):
        """
        Initialize AutoGen system with specified LLM configuration.
        
        Args:
            llm_type (str): Type of LLM to use
            workdir (str): Working directory path
            polybot_file_path (str): Path to the polybot file
        """
        self.llm_type = llm_type
        self.llm_config = get_llm_config(llm_type)
        self.workdir = workdir
        
        # Read polybot file
        with open(polybot_file_path, 'r') as polybot_file:
            self.polybot_file = ''.join(polybot_file.readlines())
        
        # Initialize executor
        self.executor = LocalCommandLineCodeExecutor(
            timeout=120,
            work_dir=workdir,
        )

        self._setup_agents()
        self._setup_group_chat()
        self._setup_teachability() # enable this to add teachability
        
    def _setup_agents(self):
        """Set up all required agents with the specified LLM configuration."""

        self.code_writer_agent = ConversableAgent(
            name="code_writer_agent",
            system_message=code_writer_system_message + self.polybot_file,
            llm_config=self.llm_config,
            code_execution_config=False,
            human_input_mode="ALWAYS",
        )
        
        # Code review agent
        self.code_review_agent = ConversableAgent(
            name="code_reviewer_agent",
            system_message=f"Your task is to review the code provided by the code writer agent and provide feedback on necessary corrections. "
                           "Ensure that all required libraries are imported, and only the existing, approved operation functions are used."
                           "The only allowed libraries and operating functions are provided in the  {self.polybot_file}",
            llm_config=self.llm_config,
            code_execution_config=False,
            human_input_mode="NEVER",
        )
        
        # PDF scraper agent
        self.scraper_agent = ConversableAgent(
            name="PDFScraper",
            llm_config=self.llm_config,
            system_message="You are a PDF scrapper and you can scrape any PDF using the tools provided if a PDF is provided for context. "
                         "After reading the text you can provide specific answers based on the context of the PDF file. "
                         "Returns 'TERMINATE' when the scraping is done.",
            human_input_mode="NEVER",
        )
        
        # Admin agent - Using custom terminating agent class
        self.polybot_admin = TerminatingUserProxyAgent(
            name="admin",
            human_input_mode="ALWAYS",
            system_message="admin. You pose the task. Return 'TERMINATE' once a task is executed without any errors.",
            llm_config=self.llm_config,
            code_execution_config={"executor": self.executor},
        )
        
        # Register the PDF scraping function
        register_function(
            pdf_to_text,
            caller=self.scraper_agent,
            executor=self.polybot_admin,
            name="scrape_pdf",
            description="Scrape PDF files and return the content.",
        )
        
    def _setup_group_chat(self):
        """Set up group chat and manager."""
        self.groupchat = autogen.GroupChat(
            agents=[self.polybot_admin, self.code_writer_agent, self.code_review_agent, self.scraper_agent],
            messages=[],
            max_round=20,
            # select_speaker_auto_model_client_cls=autogen_llm.ArgoModelClient,
            select_speaker_auto_llm_config=self.llm_config
        )
        
        self.manager = autogen.GroupChatManager(groupchat=self.groupchat, llm_config=self.llm_config)
        # self.manager.register_model_client(autogen_llm.ArgoModelClient) # for using the local LLMs
        
    def _setup_teachability(self):
        """Set up teachability for the agents."""
        self.teachability = DedupTeachability(
            verbosity=0,
            reset_db=False,
            path_to_db_dir=f"./teachability_db_{self.llm_type}",
            recall_threshold=6,
            llm_config=self.llm_config
        )
        
        # Add teachability to agents
        for agent in [self.code_writer_agent, self.code_review_agent, self.manager]:
            self.teachability.add_to_agent(agent)
    
    def initiate_chat(self, prompt: str) -> Any:
        """
        Initiate a chat with the specified prompt.
        
        Args:
            prompt (str): The prompt to initiate the chat with
            
        Returns:
            Any: Chat result
        """
        return self.polybot_admin.initiate_chat(
            self.manager,
            message=prompt,
        )

# Usage example:
if __name__ == "__main__":
    workdir = "polybot_screenshots_run"
    polybot_file_path = 'n9_robot_operation_commands.py'
    llm_type = "gpt4o" #  "gpt4o" #"gpt4o-mini" # "claude_35" #"gpt4o" #"gpt4o-mini" # "claude" #'gpt4o'
    # llm_config = {"model": "claude-3-5-sonnet-20240620", 'api_key': anthropic_api_key, 'api_type': 'anthropic'}

    # Initialize the system with desired LLM
    autogen_system = AutoGenSystem(
        llm_type=llm_type,  
        workdir=workdir,
        polybot_file_path=polybot_file_path
    )
    
    # Example prompts
    prompt_1 = """Write the execution code to move the vial with PEDOT:PSS defined as polymer A to the clamp holder."""

    # Initiate chat with desired prompt
    chat_result = autogen_system.initiate_chat(prompt_1)