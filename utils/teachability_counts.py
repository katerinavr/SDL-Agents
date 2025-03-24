import pickle
from termcolor import colored
import json
from pprint import pprint

def visualize_memories(file_path):
    """
    Read a PKL file and visualize the memories and their statistics
    
    Parameters:
        file_path (str): Path to the PKL file
    """
    try:
        # Read the PKL file
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            
        print(colored("\n=== Memory Store Statistics ===", "cyan"))
        print(f"Type of stored data: {type(data)}")
        
        # Count and display basic statistics
        if isinstance(data, dict):
            entry_count = len(data)
            print(f"Total memories: {entry_count}")
            
            # Display all memories in a formatted way
            print(colored("\n=== Stored Memories ===", "cyan"))
            for uid, (input_text, output_text) in data.items():
                print(colored(f"\nMemory ID: {uid}", "yellow"))
                print(colored("Input:", "green"))
                print(f"{input_text[:]}..." if len(input_text) > 200 else input_text)
                print(colored("Output:", "blue"))
                print(f"{output_text[:]}..." if len(output_text) > 200 else output_text)
                print("-" * 80)
                
            # Generate statistics
            stats = {
                "total_entries": entry_count,
                "memory_ids": sorted(list(data.keys())),
                "id_range": f"{min(data.keys())} to {max(data.keys())}"
            }
            
            print(colored("\n=== Detailed Statistics ===", "cyan"))
            print(f"Total memories: {stats['total_entries']}")
            print(f"Memory IDs: {stats['memory_ids']}")
            print(f"ID range: {stats['id_range']}")
            
            return stats
            
        else:
            print(colored("Unexpected data format. Expected dictionary.", "red"))
            return None
            
    except Exception as e:
        print(colored(f"Error reading pickle file: {str(e)}", "red"))
        return None

if __name__ == "__main__":
    # You can keep your existing file paths  C:\Users\kvriz\Desktop\SDL-Agents\teachability_db_gpt4o
    #teachability_db_claude_35  teachability_db_gpt4o teachability_db_gpt4o-mini
    file_path = "C:/Users/kvriz/Desktop/SDL-Agents/teachability_db_gpt4o-mini/uid_text_dict.pkl"
    stats = visualize_memories(file_path)
    
    if stats:
        print(colored("\n=== Summary ===", "cyan"))
        print(f"Successfully analyzed {stats['total_entries']} memories")