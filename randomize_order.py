import os
import random

def prepend_random_integer_to_files(folder_path):
    # Get a list of all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Generate a list of unique random integers
    unique_integers = random.sample(range(1, 300), len(files))
    
    # Rename each file by prepending a unique random integer
    for i, file_name in enumerate(files):
        new_name = f"{unique_integers[i]:03d}zz{file_name}"
        old_path = os.path.join(folder_path, file_name)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed '{file_name}' to '{new_name}'")

# Example usage
folder_path = "./Videos/"
prepend_random_integer_to_files(folder_path)