from autogen.agentchat.contrib.capabilities.teachability import Teachability, MemoStore
from termcolor import colored

class DedupMemoStore(MemoStore):
    def __init__(self, similarity_threshold: float = 0.3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.similarity_threshold = similarity_threshold
        self._clean_and_reindex()  # Clean up on initialization

    def _clean_and_reindex(self):
        """Clean up missing entries and reindex the remaining ones"""
        # Get valid entries in order
        valid_entries = []
        for uid in sorted(self.uid_text_dict.keys(), key=lambda x: int(x)):
            try:
                input_text, output_text = self.uid_text_dict[uid]
                # Verify if embedding exists
                self.vec_db.query(query_texts=[""], n_results=1, filter={"id": uid})
                valid_entries.append((input_text, output_text))
            except:
                continue

        if not valid_entries:
            self.last_memo_id = 0
            return

        # Clear existing data
        self.uid_text_dict.clear()
        self.vec_db.delete(delete_all=True)

        # Reset the counter
        self.last_memo_id = 0

        # Reinsert with new sequential IDs
        for input_text, output_text in valid_entries:
            self.last_memo_id += 1
            self.vec_db.add(
                documents=[input_text],
                ids=[str(self.last_memo_id)]
            )
            self.uid_text_dict[str(self.last_memo_id)] = (input_text, output_text)

    def find_similar_memory(self, input_text: str, output_text: str) -> tuple[bool, str | None]:
        """
        Find if a similar memory exists and return its ID if found.
        Returns (is_duplicate, memory_id)
        """
        if len(self.uid_text_dict) == 0:
            return False, None
            
        # Check for exact matches first
        for uid, (stored_input, stored_output) in self.uid_text_dict.items():
            if input_text == stored_input and output_text == stored_output:
                if self.verbosity >= 1:
                    print(colored("\nEXACT DUPLICATE DETECTED - WILL UPDATE", "yellow"))
                return True, uid

        # Check for semantic similarity
        try:
            results = self.vec_db.query(
                query_texts=[input_text],
                n_results=1
            )
            
            if not results["ids"][0]:
                return False, None
                
            closest_distance = results["distances"][0][0]
            closest_id = results["ids"][0][0]
            closest_input, closest_output = self.uid_text_dict[closest_id]
            
            if closest_distance < self.similarity_threshold:
                if self.verbosity >= 1:
                    print(colored(
                        f"\nSIMILAR MEMORY DETECTED (distance: {closest_distance})\n" +
                        f"Existing:\n  Input: {closest_input}\n  Output: {closest_output}\n" +
                        f"New:\n  Input: {input_text}\n  Output: {output_text}",
                        "yellow"
                    ))
                return True, closest_id
        except Exception as e:
            print(colored(f"\nError checking similarity: {str(e)}", "red"))
            
        return False, None

    def add_input_output_pair(self, input_text: str, output_text: str):
        """Add a new memory or update existing similar memory"""
        is_duplicate, memory_id = self.find_similar_memory(input_text, output_text)
        
        try:
            if is_duplicate and memory_id:
                # Remove old memory
                self.vec_db.delete(ids=[memory_id])
                del self.uid_text_dict[memory_id]
                
                if self.verbosity >= 1:
                    print(colored("\nRemoving old similar memory", "yellow"))
            
            # Add as new memory with next available ID
            self.last_memo_id += 1
            new_id = str(self.last_memo_id)
            
            # Add to vector DB
            self.vec_db.add(
                documents=[input_text],
                ids=[new_id]
            )
            
            # Add to dictionary
            self.uid_text_dict[new_id] = (input_text, output_text)
            
            if self.verbosity >= 1:
                print(colored(f"\nAdded new memory with ID {new_id}", "green"))
            
            # Save the updated dictionary
            self._save_memos()
            
            return True
            
        except Exception as e:
            print(colored(f"\nError adding/updating memory: {str(e)}", "red"))
            # Attempt to clean up in case of partial failure
            self._clean_and_reindex()
            return False

    def get_related_memos(self, query_text: str, n_results: int = None, **kwargs) -> list:
        try:
            # Ensure n_results is at least 1
            if not n_results or n_results < 1:
                n_results = 1
                
            results = self.vec_db.query(
                query_texts=[query_text],
                n_results=n_results
            )
            
            memo_list = []
            for i, uid in enumerate(results["ids"][0]):
                try:
                    input_text, output_text = self.uid_text_dict[uid]
                    memo_list.append((input_text, output_text))
                except KeyError:
                    print(colored(f"\nWarning: Could not find memo with ID {uid}", "yellow"))
                    continue
                    
            return memo_list
            
        except Exception as e:
            print(colored(f"\nError in get_related_memos: {str(e)}", "red"))
            return []

class DedupTeachability(Teachability):
    def __init__(self, similarity_threshold: float = 0.3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.memo_store = DedupMemoStore(
            similarity_threshold=similarity_threshold,
            verbosity=self.verbosity,
            path_to_db_dir=self.path_to_db_dir
        )