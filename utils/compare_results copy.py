import pickle
from termcolor import colored
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from chromadb import PersistentClient
import pandas as pd
import os 

def load_embeddings_from_chroma(db_path):
    """Load embeddings from a ChromaDB database"""
    try:
        # Check if the directory exists
        if not os.path.exists(db_path):
            print(colored(f"Path does not exist: {db_path}", "red"))
            return None
            
        # Get full path to the chroma.sqlite3 file
        chroma_path = os.path.join(db_path, "d88d2b31-e4af-4e95-b712-78363f40e387")
        if not os.path.exists(chroma_path):
            print(colored(f"Chroma directory not found at: {chroma_path}", "red"))
            return None
            
        client = PersistentClient(path=db_path)
        collections = client.list_collections()
        
        if len(collections) == 0:
            print(colored(f"No collections found in {db_path}", "red"))
            return None
            
        collection = client.get_collection(collections[0].name)
        results = collection.get(include=['embeddings', 'documents'])
        
        if len(results['embeddings']) == 0:
            print(colored(f"No embeddings found in {db_path}", "red"))
            return None
            
        return results['embeddings']
        
    except Exception as e:
        print(colored(f"Error loading ChromaDB from {db_path}: {str(e)}", "red"))
        return None

def compute_embedding_correlations(embeddings1, embeddings2, embeddings3, names):
    """Compute correlation between embeddings from different models"""
    
    # Convert embeddings to matrices
    matrices = []
    matrix_lengths = []
    for emb in [embeddings1, embeddings2, embeddings3]:
        if emb is not None:
            matrix = np.array(emb)
            matrices.append(matrix)
            matrix_lengths.append(len(matrix))
        else:
            print(colored("Missing embeddings for one of the models", "red"))
            return None, None
    
    print(f"\nNumber of embeddings per model:")
    for name, length in zip(names, matrix_lengths):
        print(f"{name}: {length} embeddings")
    
    # Find minimum number of embeddings to compare
    min_length = min(matrix_lengths)
    print(f"\nUsing first {min_length} embeddings from each model for fair comparison")
    
    # Truncate matrices to same length
    matrices = [matrix[:min_length] for matrix in matrices]
    
    # Compute pairwise correlations between corresponding embeddings
    pairwise_corrs = np.zeros((3, 3))
    for i in range(3):
        for j in range(3):
            # Compute correlation for each corresponding pair of embeddings
            corrs = []
            for k in range(min_length):
                corr = np.corrcoef(matrices[i][k], matrices[j][k])[0, 1]
                corrs.append(corr)
            pairwise_corrs[i, j] = np.mean(corrs)
    
    # Create correlation matrix visualization
    plt.figure(figsize=(10, 8))
    sns.heatmap(pairwise_corrs, 
                annot=True, 
                cmap='coolwarm', 
                xticklabels=names,
                yticklabels=names,
                vmin=-1, vmax=1)
    plt.title('Average Embedding Correlation Matrix')
    plt.tight_layout()
    plt.show()
    
    # Additional embedding statistics
    stats = {}
    for name, matrix in zip(names, matrices):
        stats[name] = {
            'dimension': matrix.shape[1],
            'mean': float(np.mean(matrix)),
            'std': float(np.std(matrix)),
            'min': float(np.min(matrix)),
            'max': float(np.max(matrix)),
            'num_embeddings': len(matrix)
        }
        
        # Add distribution plot
        plt.figure(figsize=(10, 4))
        plt.hist(matrix.flatten(), bins=50, alpha=0.7)
        plt.title(f'Embedding Distribution for {name}')
        plt.xlabel('Embedding Value')
        plt.ylabel('Frequency')
        plt.show()
    
    return pairwise_corrs, stats

def compare_embeddings(gpt4o_mini_path, claude35_path, gpt4o_path):
    """Compare embeddings from three different models"""
    
    print(colored("\nLoading embeddings...", "cyan"))
    names = ["GPT-4-Mini", "Claude-3.5", "GPT-4"]
    
    # Load embeddings
    embeddings = []
    for path in [gpt4o_mini_path, claude35_path, gpt4o_path]:
        emb = load_embeddings_from_chroma(path)
        embeddings.append(emb)
        if emb is None:
            print(colored(f"Failed to load embeddings from {path}", "red"))
            return None, None
    
    print(colored("\n=== Embedding Analysis ===", "cyan"))
    
    # Compute and visualize correlations
    corr_matrix, stats = compute_embedding_correlations(
        embeddings[0], embeddings[1], embeddings[2], names
    )
    
    if stats:
        # Print embedding statistics
        print(colored("\n=== Embedding Statistics ===", "yellow"))
        for name, stat in stats.items():
            print(f"\n{name}:")
            for key, value in stat.items():
                print(f"{key}: {value}")

    return corr_matrix, stats

# # if __name__ == "__main__":
# #     # Base paths for each model C:\Users\kvriz\Desktop\SDL-Agents\utils\teachability_db_claude_35
# #     gpt4o_mini_base = "C:/Users/kvriz/Desktop/SDL-Agents/utils/teachability_db_gpt-4o-mini"
# #     claude35_base = "C:/Users/kvriz/Desktop/SDL-Agents/utils/teachability_db_claude_35"
# #     gpt4o_base = "C:/Users/kvriz/Desktop/SDL-Agents/utils/teachability_db_gpt-4o"
    
# #     corr_matrix, stats = compare_embeddings(gpt4o_mini_base, claude35_base, gpt4o_base)

# if __name__ == "__main__":
#     # Update paths based on your directory structure
#     gpt4o_mini_path = "C:/Users/kvriz/Desktop/SDL-Agents/utils/teachability_db_gpt-4o-mini"
#     claude35_path = "C:/Users/kvriz/Desktop/SDL-Agents/utils/teachability_db_claude_35"
#     gpt4o_path = "C:/Users/kvriz/Desktop/SDL-Agents/utils/teachability_db_gpt-4o"

#     # Test loading each database
#     print(colored("\nTesting database loading...", "cyan"))
    
#     for path in [gpt4o_path, claude35_path, gpt4o_mini_path]:
#         print(f"\nTrying to load: {path}")
#         embeddings = load_embeddings_from_chroma(path)
#         if embeddings is not None:
#             print(f"Successfully loaded {len(embeddings)} embeddings")
#             print(f"Embedding dimension: {len(embeddings[0])}")

#     # Ask to proceed with comparison
#     proceed = input("\nDo you want to proceed with the full comparison? (y/n): ")
#     if proceed.lower() == 'y':
#         corr_matrix, stats = compare_embeddings(gpt4o_mini_path, claude35_path, gpt4o_path)


import pickle
from termcolor import colored
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from chromadb import PersistentClient
import pandas as pd
import os

def get_first_uuid_dir(base_path):
    """Get the first UUID directory in the base path"""
    try:
        # List all directories and find the first that looks like a UUID
        for item in os.listdir(base_path):
            if len(item) == 36 and item.count('-') == 4:  # Simple UUID check
                return os.path.join(base_path, item)
        return None
    except Exception as e:
        print(colored(f"Error finding UUID directory: {str(e)}", "red"))
        return None

def load_embeddings_from_chroma(db_path):
    """Load embeddings from a ChromaDB database"""
    try:
        # Check if the directory exists
        if not os.path.exists(db_path):
            print(colored(f"Path does not exist: {db_path}", "red"))
            return None
            
        # Find UUID directory
        uuid_dir = get_first_uuid_dir(db_path)
        if not uuid_dir:
            print(colored(f"No UUID directory found in: {db_path}", "red"))
            return None
            
        print(f"Found UUID directory: {uuid_dir}")
            
        client = PersistentClient(path=db_path)
        collections = client.list_collections()
        
        if len(collections) == 0:
            print(colored(f"No collections found in {db_path}", "red"))
            return None
            
        collection = client.get_collection(collections[0].name)
        results = collection.get(include=['embeddings', 'documents'])
        
        if len(results['embeddings']) == 0:
            print(colored(f"No embeddings found in {db_path}", "red"))
            return None
            
        return results['embeddings']
        
    except Exception as e:
        print(colored(f"Error loading ChromaDB from {db_path}: {str(e)}", "red"))
        return None

if __name__ == "__main__":
    # Update paths to correct locations (remove 'utils' from path)
    gpt4o_path = "C:/Users/kvriz/Desktop/SDL-Agents/utils/teachability_db_gpt-4o"
    claude35_path = "C:/Users/kvriz/Desktop/SDL-Agents/utils/teachability_db_claude_35"
    gpt4o_mini_path = "C:/Users/kvriz/Desktop/SDL-Agents/utils/teachability_db_gpt-4o-mini"  # Note: fixed hyphen to underscore

    # Print current working directory for debugging
    print(f"Current working directory: {os.getcwd()}")
    
    # Test loading each database
    print(colored("\nTesting database loading...", "cyan"))
    
    for path in [gpt4o_path, claude35_path, gpt4o_mini_path]:
        print(f"\nTrying to load: {path}")
        if os.path.exists(path):
            print(f"Directory exists: {path}")
            print(f"Contents: {os.listdir(path)}")
        embeddings = load_embeddings_from_chroma(path)
        if embeddings is not None:
            print(f"Successfully loaded {len(embeddings)} embeddings")
            print(f"Embedding dimension: {len(embeddings[0])}")

    # Ask to proceed with comparison
    proceed = input("\nDo you want to proceed with the full comparison? (y/n): ")
    if proceed.lower() == 'y':
        corr_matrix, stats = compare_embeddings(gpt4o_mini_path, claude35_path, gpt4o_path)