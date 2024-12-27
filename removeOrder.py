import os

def remove_prefix_before_zz(folder_path):
    # Get a list of all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Rename each file by removing "zz" and everything before it
    for file_name in files:
        if "zz" in file_name:
            new_name = file_name.split("zz", 1)[1]
            old_path = os.path.join(folder_path, file_name)
            new_path = os.path.join(folder_path, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed '{file_name}' to '{new_name}'")

# Example usage
folder_path = "./Videos/"
remove_prefix_before_zz(folder_path)