import os
import shutil

def clear_folders():
    folders = ['HR', 'LR']
    
    for folder in folders:
        try:
            if os.path.exists(folder):
                # Remove all files in the folder
                shutil.rmtree(folder)
                # Recreate empty folder
                os.makedirs(folder)
                print(f"Cleared contents of {folder} folder")
            else:
                print(f"Folder {folder} does not exist")
        except Exception as e:
            print(f"Error clearing {folder} folder: {str(e)}")

if __name__ == "__main__":
    clear_folders()