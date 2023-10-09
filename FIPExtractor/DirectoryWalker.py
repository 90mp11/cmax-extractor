import os

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