import pickle
from termcolor import colored
from collections import defaultdict
import difflib

def load_memory_database(file_path):
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(colored(f"Error loading {file_path}: {str(e)}", "red"))
        return None

def compare_memory_databases(gpt4o_mini_path, claude35_path, gpt4o_path):
    """Compare three memory databases and analyze their differences"""
    
    # Load all databases
    dbs = {
        "GPT-4-Mini": load_memory_database(gpt4o_mini_path),
        "Claude-3.5": load_memory_database(claude35_path),
        "GPT-4": load_memory_database(gpt4o_path)
    }
    
    print(colored("\n=== Memory Database Comparison ===", "cyan"))
    
    # Basic statistics
    stats = {}
    for name, db in dbs.items():
        if db:
            stats[name] = {
                "total_memories": len(db),
                "memory_ids": sorted(list(db.keys())),
                "unique_inputs": len(set(input_text for input_text, _ in db.values())),
                "unique_outputs": len(set(output_text for _, output_text in db.values())),
                "avg_input_length": sum(len(input_text) for input_text, _ in db.values()) / len(db),
                "avg_output_length": sum(len(output_text) for _, output_text in db.values()) / len(db)
            }
    
    # Print comparative statistics
    print(colored("\n=== Basic Statistics ===", "yellow"))
    for name, stat in stats.items():
        print(f"\n{name}:")
        print(f"Total memories: {stat['total_memories']}")
        print(f"Unique inputs: {stat['unique_inputs']}")
        print(f"Unique outputs: {stat['unique_outputs']}")
        print(f"Average input length: {stat['avg_input_length']:.2f} characters")
        print(f"Average output length: {stat['avg_output_length']:.2f} characters")

    # Compare responses to same inputs
    print(colored("\n=== Response Comparison for Same Inputs ===", "yellow"))
    common_inputs = defaultdict(dict)
    
    # Collect responses for same inputs
    for name, db in dbs.items():
        if db:
            for _, (input_text, output_text) in db.items():
                common_inputs[input_text][name] = output_text

    # Find inputs that have responses from multiple models
    shared_inputs = [input_text for input_text, responses in common_inputs.items() 
                    if len(responses) > 1]
    
    if shared_inputs:
        print(f"\nFound {len(shared_inputs)} inputs with multiple responses")
        for input_text in shared_inputs[:5]:  # Show first 5 examples
            print(colored(f"\nInput:", "green"))
            print(input_text[:200] + "..." if len(input_text) > 200 else input_text)
            
            responses = common_inputs[input_text]
            for model, response in responses.items():
                print(colored(f"\n{model} response:", "blue"))
                print(response[:200] + "..." if len(response) > 200 else response)
            print("-" * 80)
    else:
        print("No common inputs found across databases")

    return stats

if __name__ == "__main__":
    gpt4o_mini_path = "C:/Users/kvriz/Desktop/SDL-Agents/teachability_db_gpt4o-mini/uid_text_dict.pkl"
    claude35_path = "C:/Users/kvriz/Desktop/SDL-Agents/teachability_db_claude_35/uid_text_dict.pkl"
    gpt4o_path = "C:/Users/kvriz/Desktop/SDL-Agents/teachability_db_gpt4o/uid_text_dict.pkl"

    comparison_stats = compare_memory_databases(gpt4o_mini_path, claude35_path, gpt4o_path)