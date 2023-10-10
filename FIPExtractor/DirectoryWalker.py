import os
import shutil

# DirectoryWalker Class for directory traversal
class DirectoryWalker:
    @staticmethod
    def find_eligible_files(folder_path, file_extension):
        eligible_files = []
        for root, _, files in os.walk(folder_path):
            for filename in files:
                if filename.lower().endswith(file_extension):
                    eligible_files.append(os.path.join(root, filename))
        return eligible_files
    
    def delete_folder_contents(folder_path):
        """
        Deletes all files and folders within the given folder path.
        
        Parameters:
            folder_path (str): The path to the folder whose contents are to be deleted.
            
        Returns:
            bool: True if successful, False otherwise.
            str: Error message if unsuccessful, None otherwise.
        """
        try:
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            return True, None
        except Exception as e:
            return False, str(e)