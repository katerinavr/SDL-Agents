import pickle
from termcolor import colored
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from chromadb import PersistentClient
import pandas as pd
import os 
import scipy

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


def compute_correlation(emb1, emb2, method='pearson', use_abs=False):
    """
    Compute correlation between two embeddings using specified method
    
    Parameters:
    - emb1, emb2: numpy arrays of embedding vectors
    - method: string, one of ['pearson', 'spearman', 'cosine']
    - use_abs: if True, return absolute value of correlation
    
    Returns:
    - correlation value
    """
    if method == 'pearson':
        corr = np.corrcoef(emb1, emb2)[0, 1]
    elif method == 'spearman':
        corr = scipy.stats.spearmanr(emb1, emb2)[0]
    elif method == 'cosine':
        corr = 1 - scipy.spatial.distance.cosine(emb1, emb2)
    else:
        raise ValueError(f"Unknown correlation method: {method}")
        
    return np.abs(corr) if use_abs else corr

def compute_index_correlations(embeddings1, embeddings2, embeddings3, names, correlation_method='pearson', use_abs=False):
    """
    Compute correlations between all embedding indices using specified correlation method
    """
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
    
    # Find minimum number of embeddings to compare
    min_length = min(matrix_lengths)
    print(f"\nUsing first {min_length} embeddings from each model for fair comparison")
    print(f"Using correlation method: {correlation_method}")
    print(f"Using absolute values: {use_abs}")
    
    # Truncate matrices to same length
    matrices = [matrix[:min_length] for matrix in matrices]
    
    # Create correlation matrix for all indices across all models
    total_indices = min_length * len(matrices)
    full_corr_matrix = np.zeros((total_indices, total_indices))
    
    # Compute correlations between all indices
    for model1_idx in range(len(matrices)):
        for model2_idx in range(len(matrices)):
            for i in range(min_length):
                for j in range(min_length):
                    # Calculate global indices
                    global_i = model1_idx * min_length + i
                    global_j = model2_idx * min_length + j
                    
                    # Get embeddings
                    emb1 = matrices[model1_idx][i]
                    emb2 = matrices[model2_idx][j]
                    
                    # Compute correlation using specified method
                    corr = compute_correlation(emb1, emb2, correlation_method, use_abs)
                    full_corr_matrix[global_i, global_j] = corr
    
    # Create labels for the heatmap
    labels = []
    for model_name in names:
        labels.extend([f"{model_name}_{i}" for i in range(min_length)])
    
    # Set visualization parameters based on whether using absolute values
    vmin = 0 if use_abs else (-1 if correlation_method != 'cosine' else 0)
    vmax = 1
    cmap = 'viridis' if use_abs else 'coolwarm'
    
    # Visualize full correlation matrix
    plt.figure(figsize=(20, 20))
    sns.heatmap(full_corr_matrix,
                cmap=cmap,
                xticklabels=labels,
                yticklabels=labels,
                vmin=vmin,
                vmax=vmax)
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    title = f'Full Index-by-Index {correlation_method.title()} Correlation Matrix'
    if use_abs:
        title += ' (Absolute Values)'
    plt.title(title)
    plt.tight_layout()
    plt.savefig('memory_stats.png', dpi=600 )
    plt.show()
    
    # Compute statistics
    stats = {
        'correlation_method': correlation_method,
        'using_absolute_values': use_abs,
        'mean_correlation': np.mean(full_corr_matrix),
        'std_correlation': np.std(full_corr_matrix),
        'min_correlation': np.min(full_corr_matrix),
        'max_correlation': np.max(full_corr_matrix),
        'median_correlation': np.median(full_corr_matrix),
        'num_indices_per_model': min_length,
        'total_indices': total_indices
    }
    
    # Add model-specific statistics
    for i, name in enumerate(names):
        start_idx = i * min_length
        end_idx = (i + 1) * min_length
        model_corrs = full_corr_matrix[start_idx:end_idx, start_idx:end_idx]
        stats[f'{name}_internal_mean_correlation'] = np.mean(model_corrs)
        stats[f'{name}_internal_std_correlation'] = np.std(model_corrs)
    
    return full_corr_matrix, stats

def compare_embeddings(gpt4o_mini_path, claude35_path, gpt4o_path, correlation_method='pearson', use_abs=False):
    """
    Compare embeddings from three different models using specified correlation method
    """
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
    corr_matrix, stats = compute_index_correlations(
        embeddings[0], embeddings[1], embeddings[2], names, correlation_method, use_abs
    )
    
    if stats:
        # Print statistics
        title = f"{correlation_method.title()} Correlation Statistics"
        if use_abs:
            title += " (Absolute Values)"
        print(colored(f"\n=== {title} ===", "yellow"))
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"{key}: {value:.4f}")
            else:
                print(f"{key}: {value}")
    
    return corr_matrix, stats


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
    # gpt4o_path = "C:/Users/kvriz/Desktop/SDL-Agents/teachability_db_gpt4o"
    # claude35_path = "C:/Users/kvriz/Desktop/SDL-Agents/teachability_db_claude_35"
    # gpt4o_mini_path = "C:/Users/kvriz/Desktop/SDL-Agents/teachability_db_gpt4o-mini"  

    gpt4o_path = "C:/Users/kvriz/Desktop/SDL-Agents/teachability_db_gpt4o"
    claude35_path = "C:/Users/kvriz/Desktop/SDL-Agents/teachability_db_claude_35"
    gpt4o_mini_path = "C:/Users/kvriz/Desktop/SDL-Agents/teachability_db_gpt4o-mini"  

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
        corr_matrix, stats = compare_embeddings(gpt4o_mini_path, claude35_path, gpt4o_path, use_abs=True, correlation_method='cosine')