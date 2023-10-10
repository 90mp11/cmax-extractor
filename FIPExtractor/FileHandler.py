import zipfile

class FileHandler:
    @staticmethod
    def read_binary_file(file_path):
        try:
            with open(file_path, 'rb') as file:
                return file.read(), None
        except Exception as e:
            return None, str(e)
        
    @staticmethod
    def write_image(image, save_path):
        try:
            image.save(save_path)
            return save_path, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def unzip_files(zip_file_path, temp_folder):
        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                cmax2_files = [file for file in zip_ref.namelist() if file.lower().endswith('.cmax2')]
                for file in cmax2_files:
                    zip_ref.extract(file, temp_folder)
            return True, None
        except Exception as e:
            return False, str(e)
