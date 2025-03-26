import gradio as gr
import os
import json
from typing import List, Tuple
from sdl_agents import AutoGenSystem
import autogen
os.environ["GRADIO_ANALYTICS_ENABLED"] = "False" # to avoid the timed out

# GroupChatManager to capture messages
class CaptureGroupChatManager(autogen.GroupChatManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.captured_messages = []
        
    def receive(self, message, sender, request_reply=None, silent=False):
        # Capture the message
        if not silent:
            agent_name = getattr(sender, "name", "Unknown")
            if isinstance(message, dict) and "content" in message:
                content = message["content"]
            else:
                content = str(message)
                
            if content:  
                self.captured_messages.append(f"{agent_name}: {content}")
        
        return super().receive(message, sender, request_reply, silent)

# Initialize AutoGen system
workdir = "polybot_screenshots_run"
os.makedirs(workdir, exist_ok=True)
polybot_file_path = 'n9_robot_operation_commands.py'
llm_type = "gpt4o"  

# Create the AutoGen system
autogen_system = None 

# Store conversation history
conversation_history = []

def ensure_autogen_system():
    """Make sure the AutoGen system is initialized"""
    global autogen_system
    if autogen_system is None:
        # Create the system only when needed (first message)
        autogen_system = AutoGenSystem(
            llm_type=llm_type,
            workdir=workdir,
            polybot_file_path=polybot_file_path
        )
        
        # Set all agents to NEVER ask for human input
        autogen_system.code_writer_agent.human_input_mode = "ALWAYS"
        autogen_system.code_review_agent.human_input_mode = "NEVER"
        autogen_system.scraper_agent.human_input_mode = "NEVER"
        autogen_system.polybot_admin.human_input_mode = "ALWAYS"
        
        # Replace the manager with our capturing version
        autogen_system.manager = CaptureGroupChatManager(
            groupchat=autogen_system.groupchat, 
            llm_config=autogen_system.llm_config
        )

def process_message(message: str, history: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        
    print('autogen system initiallization')
    ensure_autogen_system()
    
    autogen_system.manager.captured_messages = []
    
    updated_history = history.copy() 
    updated_history.append((message, "Processing your request..."))
    
    
    try:
        autogen_system.initiate_chat(message)
        
        # Get the conversation output
        response = "\n\n".join(autogen_system.manager.captured_messages)
        # print('response', response)
        if not response:
            response = "The agents processed your request but didn't generate a visible response. Try another query or check console output."
            
    except Exception as e:
        response = f"Error: {str(e)}"
        print(f"Exception during chat: {e}")
    
    # Update the last message with the actual response
    updated_history[-1] = (message, response)
    
    # Store in global history
    conversation_history.append((message, response))
    
    return updated_history

def clear_history():
    """Clear the conversation history"""
    global conversation_history
    conversation_history = []
    return []

def upload_pdf(file_path):
    """Handle PDF file upload"""
    # Save the uploaded PDF file
    if file_path is not None:
        filename = os.path.basename(file_path.name)
        save_path = os.path.join(workdir, filename)
        with open(save_path, 'wb') as f:
            f.write(file_path.read())
        return f"PDF uploaded: {filename}"
    return "No file uploaded"

# Gradio interface
with gr.Blocks(title="SDL Agent Chat") as demo:
    gr.Markdown("# SDL Agents Chat Interface")
    gr.Markdown("Upload a PDF file for context (optional) and start chatting with the AutoGen agents.")
    
    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(
                height=500,
                show_label=False,
                elem_id="chatbot"
            )
            
            with gr.Row():
                msg = gr.Textbox(
                    placeholder="Enter your message here...",
                    show_label=False,
                    container=False
                )
                submit_btn = gr.Button("Submit", variant="primary")
            
            with gr.Row():
                clear_btn = gr.Button("Clear History", variant="secondary")
                
        with gr.Column(scale=1):
            pdf_upload = gr.File(
                label="Upload PDF",
                file_types=[".pdf"],
                type="filepath"
            )
            pdf_status = gr.Textbox(label="Upload Status", interactive=False)
    
    submit_btn.click(
        process_message, 
        inputs=[msg, chatbot], 
        outputs=[chatbot]
    ).then(
        lambda: "", 
        None, 
        msg
    )
    
    clear_btn.click(
        clear_history,
        outputs=[chatbot]
    )
    
    pdf_upload.upload(
        upload_pdf,
        inputs=[pdf_upload],
        outputs=[pdf_status]
    )
    
    msg.submit(
        process_message, 
        inputs=[msg, chatbot], 
        outputs=[chatbot]
    ).then(
        lambda: "", 
        None, 
        msg
    )


# # Launch the app
demo.launch(share=False, debug=True)  
# conversation_history = []
# msg = "move the vial with PEDOT:PSS defined as polymer A to the clamp holder"
# # print(msg)
# process_message(message = msg, history=conversation_history)