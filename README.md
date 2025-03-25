A repository for implementing and testing an autonomous agentic pipeline on a real robotic environment using an N9 robotic station (https://www.northrobotics.com/robots).



### Installation

1. Clone the repository:
```bash
git clone https://github.com/katerinavr/SDL-Agents.git
cd SDL-Agents
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Add the API keys (config/settings.py):
```bash
OPENAI_API_KEY = ""
anthropic_api_key = ""
```

## Components

### Core Files
- `autogen_llm.py`: Enables the connection with local LLMs 
- `n9_robot_operation_commands.py`: Defines the set of available robot operation commands
- `params.py`: Contains configuration parameters and settings for the system
- `sdl_agents.py`: Main implementation of SDL agents

### Teachability Databases
- `teachability_db_claude_35/`: Contains the ChromaDB with the saved input-output pairs after the human teachings using as a base model Claude-3.5-Sonnet
- `teachability_db_gpt4o/`: Contains the ChromaDB with the saved input-output pairs after the human teachings using as a base model GPT-4o
- `teachability_db_gpt4o-mini/`: Contains the ChromaDB with the saved input-output pairs after the human teachings using as a base model GPT-4o-mini

## Examples

- `notebooks`: Contain examples of using the agentic pipeline to operate the N9 robot will tasks of increased complexity.